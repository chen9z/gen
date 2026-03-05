from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from .diff_renderer import extract_file_change_info, render_diff, summarize_diff
from .syntax_highlighter import StreamingSyntaxHighlighter
from .tool_key_args import extract_key_arg_from_json, extract_tool_key_arg, normalize_tool_name

LIVE_CHAR_LIMIT = 8000


@dataclass(slots=True)
class ToolcallPreview:
    name: str = ""
    args: str = ""
    _name_parts: list[str] = field(default_factory=list, init=False)
    _args_parts: list[str] = field(default_factory=list, init=False)

    def append_name(self, delta: str) -> None:
        """Efficiently append to name using list accumulation."""
        if delta:
            self._name_parts.append(delta)
            self.name = "".join(self._name_parts)

    def append_args(self, delta: str) -> None:
        """Efficiently append to args using list accumulation."""
        if delta:
            self._args_parts.append(delta)
            self.args = "".join(self._args_parts)


@dataclass(slots=True)
class AssistantBlock:
    text: str = ""
    thinking: str = ""
    toolcalls: dict[int, ToolcallPreview] = field(default_factory=dict)
    error: str | None = None
    done: bool = False
    usage_text: str = ""
    _highlighter: StreamingSyntaxHighlighter = field(default_factory=StreamingSyntaxHighlighter, init=False)
    _text_parts: list[str] = field(default_factory=list, init=False)
    _thinking_parts: list[str] = field(default_factory=list, init=False)
    _cached_render: RenderableType | None = field(default=None, init=False)

    def has_content(self) -> bool:
        return bool(self.text or self.thinking or self.toolcalls or self.error)

    def append_text(self, delta: str) -> None:
        """Efficiently append to text using list accumulation."""
        if delta:
            self._text_parts.append(delta)
            self.text = "".join(self._text_parts)
            self._highlighter.append(delta)

    def append_thinking(self, delta: str) -> None:
        """Efficiently append to thinking using list accumulation."""
        if delta:
            self._thinking_parts.append(delta)
            self.thinking = "".join(self._thinking_parts)

    def _ensure_toolcall(self, content_index: int) -> ToolcallPreview:
        preview = self.toolcalls.get(content_index)
        if preview is None:
            preview = ToolcallPreview()
            self.toolcalls[content_index] = preview
        return preview

    def append_toolcall_name(self, content_index: int, delta: str) -> None:
        if not delta:
            return
        self._ensure_toolcall(content_index).append_name(delta)

    def append_toolcall_args(self, content_index: int, delta: str) -> None:
        if not delta:
            return
        self._ensure_toolcall(content_index).append_args(delta)

    def set_toolcall_from_message(self, content_index: int, name: str, args_json: str) -> None:
        self.toolcalls[content_index] = ToolcallPreview(name=name, args=args_json)

    def finish(self) -> None:
        self.done = True
        # Clear accumulated lists to free memory (keep only final strings)
        self._text_parts.clear()
        self._thinking_parts.clear()
        self._highlighter.clear_buffer()

    @staticmethod
    def _single_line_preview(text: str, limit: int = 140) -> str:
        collapsed = " ".join(part for part in text.strip().split())
        if len(collapsed) <= limit:
            return collapsed
        return collapsed[: limit - 3] + "..."

    def set_usage_text(self, text: str) -> None:
        """Set usage text and invalidate cached render."""
        self.usage_text = text
        self._cached_render = None

    def render(self) -> RenderableType:
        # Use cached render for completed blocks
        if self.done and self._cached_render is not None:
            return self._cached_render

        parts: list[RenderableType] = []

        # P10: Only show thinking spinner when no text is streaming yet
        if self.thinking and not self.done and not self.text:
            parts.append(Spinner("dots", text="Thinking...", style="dim italic"))

        if self.text:
            if self.done:
                parts.append(Markdown(self.text))
            else:
                # Use streaming syntax highlighting if code blocks detected
                if self._highlighter.has_code_blocks():
                    highlighted = self._highlighter.render_highlighted()
                    parts.extend(highlighted)
                    parts.append(Text("▍"))
                else:
                    parts.append(Text(self.text + "▍"))
        elif not self.done and not self.thinking:
            parts.append(Spinner("dots", text="Thinking...", style="dim italic"))

        # P11: Only show toolcall preview during streaming, not after done
        if self.toolcalls and not self.done:
            preview = sorted(self.toolcalls.items())[-1][1]  # only last one
            name = preview.name.strip()
            if name:
                key_arg = extract_key_arg_from_json(name, preview.args)
                tc = Text()
                tc.append("  ⏺ ", style="dim cyan")
                tc.append(normalize_tool_name(name), style="bold")
                if key_arg:
                    tc.append(f" {key_arg}", style="dim")
                parts.append(tc)

        if self.error:
            parts.append(Text(f"Error: {self.error}", style="red"))

        if self.usage_text and self.done and (self.text or self.error):
            parts.append(Text(self.usage_text, style="dim"))

        result = Group(*parts) if parts else Text("")

        # Cache the render result for completed blocks
        if self.done:
            self._cached_render = result

        return result


@dataclass(slots=True)
class ToolRunBlock:
    tool_call_id: str
    name: str
    args: dict[str, Any]
    status: str = "running"
    is_error: bool = False
    result_summary: str | None = None
    error_detail: str | None = None
    result: Any = None
    start_time: float = 0.0
    duration: float = 0.0
    _show_details: bool = False
    _show_diff: bool = False

    def mark_done(
        self,
        *,
        is_error: bool,
        result_summary: str | None = None,
        error_detail: str | None = None,
        result: Any = None,
    ) -> None:
        self.status = "done"
        self.is_error = is_error
        self.result_summary = result_summary
        self.error_detail = error_detail
        self.result = result
        if self.start_time > 0:
            import time
            self.duration = time.time() - self.start_time

    def toggle_details(self) -> None:
        """Toggle error details visibility."""
        self._show_details = not self._show_details

    def toggle_diff(self) -> None:
        """Toggle diff visibility."""
        self._show_diff = not self._show_diff

    def _key_arg(self) -> str:
        return extract_tool_key_arg(self.name, self.args)

    def render(self) -> RenderableType:
        key_arg = self._key_arg()
        display_name = normalize_tool_name(self.name)

        if self.status == "running":
            label = Text()
            label.append(f"  {display_name}", style="bold")
            if key_arg:
                label.append(f" {key_arg}", style="dim")
            return Spinner("dots", text=label)

        line = Text()
        if self.is_error:
            line.append("  ✗ ", style="red")
        else:
            line.append("  ✓ ", style="green")
        line.append(display_name, style="bold")
        if key_arg:
            line.append(f" {key_arg}", style="dim")
        if self.duration > 0.1:
            line.append(f" ({self.duration:.2f}s)", style="dim")

        # P2: Compute change_info once, reuse below
        change_info = None
        if not self.is_error and self.result:
            change_info = extract_file_change_info(self.name, self.args, self.result)
            if change_info:
                file_path, old_content, new_content = change_info
                diff_summary = summarize_diff(old_content, new_content)
                line.append(f" [{diff_summary}]", style="cyan dim")

        if self.is_error and self.result_summary:
            line.append(f" - {self.result_summary}", style="dim")

        # Add visual indicators for expandable content
        if self.is_error and self.error_detail:
            indicator = "▼" if self._show_details else "▶"
            line.append(f" {indicator}", style="dim")
        elif change_info is not None:
            indicator = "▼" if self._show_diff else "▶"
            line.append(f" {indicator}", style="dim")

        parts: list[RenderableType] = [line]

        # Show error details if available and expanded
        if self.is_error and self.error_detail and self._show_details:
            detail_text = Text(self.error_detail, style="red dim")
            parts.append(Panel(detail_text, title="Error Details", border_style="red"))

        # Show diff if available and expanded
        if not self.is_error and self._show_diff and change_info:
            file_path, old_content, new_content = change_info
            diff_view = render_diff(old_content, new_content, file_path)
            parts.append(Panel(diff_view, title=f"Diff: {file_path}", border_style="cyan"))

        return Group(*parts) if len(parts) > 1 else line


@dataclass(slots=True)
class UserPromptBlock:
    content: str

    def render(self) -> RenderableType:
        t = Text()
        t.append("❯ ", style="bold magenta")
        t.append(self.content, style="bold")
        return t


@dataclass(slots=True)
class NoticeBlock:
    level: str
    content: str

    def render(self) -> RenderableType:
        style = {"info": "cyan", "warning": "yellow", "error": "red"}.get(self.level, "cyan")
        return Text(self.content, style=style)
