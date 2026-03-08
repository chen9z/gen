from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.table import Table
from rich.spinner import Spinner
from rich.text import Text

from .diff_renderer import extract_file_change_info, render_diff, summarize_diff
from .tool_key_args import extract_key_arg_from_json, extract_tool_key_arg, normalize_tool_name

_ASSISTANT_DOT_STYLE = "bold white"
_TOOL_SUCCESS_DOT_STYLE = "bold green"
_TOOL_ERROR_DOT_STYLE = "bold red"
_USER_STRIP_STYLE = "on #1b2130"
_USER_LABEL_STYLE = "bold #f3f4f6"
_USER_TEXT_STYLE = "#e5e7eb"
_THINKING_STYLE = "italic #9ca3af"


def _two_column_row(leading: RenderableType, body: RenderableType, *, style: str | None = None) -> RenderableType:
    table = Table.grid(expand=True)
    table.add_column(width=2)
    table.add_column(ratio=1)
    if style:
        table.style = style
    table.add_row(leading, body)
    return table


def _single_column_row(body: RenderableType, *, style: str | None = None) -> RenderableType:
    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    if style:
        table.style = style
    table.add_row(body)
    return table


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
    _text_parts: list[str] = field(default_factory=list, init=False)
    _thinking_parts: list[str] = field(default_factory=list, init=False)
    _cached_render: RenderableType | None = field(default=None, init=False)
    _show_thinking: bool = field(default=False, init=False)
    _draft_text: str = field(default="", init=False)
    _pending_segments: list[str] = field(default_factory=list, init=False)
    scrollback_done: bool = field(default=False, init=False)
    _chrome_emitted: bool = field(default=False, init=False)

    def has_content(self) -> bool:
        return bool(self.text or self.thinking or self.toolcalls or self.error)

    def append_text(self, delta: str) -> None:
        """Efficiently append to text using list accumulation."""
        if delta:
            self._text_parts.append(delta)
            self.text = "".join(self._text_parts)
            self._draft_text += delta
            self._commit_stable_text_segments()

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

    def toggle_thinking(self) -> None:
        self._show_thinking = not self._show_thinking
        self._cached_render = None  # invalidate cache

    def finish(self) -> None:
        self.done = True
        if self._draft_text:
            self._pending_segments.append(self._draft_text)
            self._draft_text = ""
        # Clear accumulated lists to free memory (keep only final strings)
        self._text_parts.clear()
        self._thinking_parts.clear()

    def has_pending_scrollback(self) -> bool:
        return bool(self._pending_segments)

    def has_live_content(self) -> bool:
        if self._draft_text:
            return True
        if self.error:
            return True
        if self.thinking:
            return True
        if self.toolcalls and not self.done:
            return True
        return not self.done and not self.thinking

    def drain_scrollback(self) -> list[RenderableType]:
        segments = self._pending_segments[:]
        self._pending_segments.clear()
        renderables: list[RenderableType] = []
        for segment in segments:
            renderables.append(self._wrap_body(self._render_text_segment(segment)))
            self._chrome_emitted = True
        return renderables

    def _commit_stable_text_segments(self) -> None:
        stable_end = self._find_stable_boundary(self._draft_text)
        if stable_end <= 0:
            return
        segment = self._draft_text[:stable_end]
        self._pending_segments.append(segment)
        self._draft_text = self._draft_text[stable_end:]

    @staticmethod
    def _find_stable_boundary(text: str) -> int:
        if not text:
            return 0
        stable_end = 0
        offset = 0
        in_code_block = False
        for line in text.splitlines(keepends=True):
            offset += len(line)
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                if not in_code_block:
                    stable_end = offset
                continue
            if not in_code_block and line.strip() == "":
                stable_end = offset
        if text.strip().endswith("```") and not in_code_block:
            stable_end = len(text)
        return stable_end

    @staticmethod
    def _render_text_segment(text: str) -> RenderableType:
        body = text.strip("\n")
        if not body:
            return Text("")
        return Markdown(body)

    def _wrap_body(self, body: RenderableType) -> RenderableType:
        leading = Text("●", style=_ASSISTANT_DOT_STYLE) if not self._chrome_emitted else Text(" ")
        return _two_column_row(leading, body)

    def render(self) -> RenderableType:
        if self.done and self._cached_render is not None:
            return self._cached_render

        parts: list[RenderableType] = []

        # Thinking display
        if self.thinking:
            parts.append(Text("Thinking...", style=_THINKING_STYLE))
            for line in self.thinking.splitlines():
                parts.append(Text(line, style=_THINKING_STYLE))

        # Main text
        if self._draft_text:
            if self.done:
                parts.append(self._render_text_segment(self._draft_text))
            else:
                parts.append(Text(self._draft_text.rstrip("\n")))
                parts.append(Text("▍"))
        elif not self.done and not self.thinking:
            parts.append(Spinner("dots", text="Thinking...", style="dim italic"))

        # Toolcall preview (streaming only)
        if self.toolcalls and not self.done:
            preview = sorted(self.toolcalls.items())[-1][1]
            name = preview.name.strip()
            if name:
                key_arg = extract_key_arg_from_json(name, preview.args)
                tc = Text()
                tc.append("⏺ ", style="dim cyan")
                tc.append(normalize_tool_name(name), style="bold")
                if key_arg:
                    tc.append(f" {key_arg}", style="dim")
                parts.append(tc)

        if self.error:
            parts.append(Text(f"✗ Error: {self.error}", style="red"))

        body = Group(*parts) if parts else Text("")
        result = self._wrap_body(body) if parts else Text("")

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
    scrollback_done: bool = False

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

    def has_live_content(self) -> bool:
        return not self.scrollback_done

    def render(self) -> RenderableType:
        key_arg = self._key_arg()
        display_name = normalize_tool_name(self.name)

        if self.status == "running":
            label = Text()
            label.append(f"{display_name}", style="bold")
            if key_arg:
                label.append(f" {key_arg}", style="dim")
            return Spinner("dots", text=label)

        # Done state
        line = Text()
        if self.is_error:
            dot_style = _TOOL_ERROR_DOT_STYLE
        else:
            dot_style = _TOOL_SUCCESS_DOT_STYLE
        line.append(display_name, style="bold")
        if key_arg:
            line.append(f" {key_arg}", style="dim")

        # Change summary inline
        change_info = None
        if not self.is_error and self.result:
            change_info = extract_file_change_info(self.name, self.args, self.result)
            if change_info:
                _file_path, old_content, new_content = change_info
                diff_summary = summarize_diff(old_content, new_content)
                line.append(f" ({diff_summary})", style="cyan dim")

        if self.duration > 0.1:
            line.append(f" ({self.duration:.1f}s)", style="dim")

        if self.is_error and self.result_summary:
            line.append(f" — {self.result_summary}", style="dim")

        parts: list[RenderableType] = [line]

        # Expandable hint on next line
        if self.is_error and self.error_detail:
            hint_text = "Hide details" if self._show_details else "Show details"
            indicator = "▼" if self._show_details else "▶"
            parts.append(Text(f"  {indicator} {hint_text}", style="dim"))
        elif change_info is not None:
            hint_text = "Hide diff" if self._show_diff else "Show diff"
            indicator = "▼" if self._show_diff else "▶"
            parts.append(Text(f"  {indicator} {hint_text}", style="dim"))

        # Expanded error details (indented, no Panel)
        if self.is_error and self.error_detail and self._show_details:
            for err_line in self.error_detail.splitlines()[:20]:
                parts.append(Text(f"    {err_line}", style="red dim"))

        # Expanded diff (indented, no Panel)
        if not self.is_error and self._show_diff and change_info:
            _file_path, old_content, new_content = change_info
            diff_view = render_diff(old_content, new_content, _file_path)
            parts.append(Text("    ", style=""))  # spacer
            parts.append(diff_view)

        body = Group(*parts) if len(parts) > 1 else line
        return _two_column_row(Text("●", style=dot_style), body)


@dataclass(slots=True)
class UserPromptBlock:
    content: str

    def render(self) -> RenderableType:
        t = Text()
        t.append("You", style=_USER_LABEL_STYLE)
        t.append("  ", style=_USER_LABEL_STYLE)
        t.append(self.content, style=_USER_TEXT_STYLE)
        return _single_column_row(t, style=_USER_STRIP_STYLE)
