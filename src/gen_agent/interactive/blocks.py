from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

LIVE_CHAR_LIMIT = 8000

_TOOL_KEY_ARGS: dict[str, list[str]] = {
    "Read": ["path"],
    "Write": ["path"],
    "Edit": ["path"],
    "Bash": ["command"],
    "Grep": ["pattern", "path"],
    "Find": ["pattern", "path"],
    "Ls": ["path"],
}


def _extract_tool_key_arg(name: str, args: dict[str, Any]) -> str:
    keys = _TOOL_KEY_ARGS.get(name, [])
    for key in keys:
        value = args.get(key)
        if isinstance(value, str) and value.strip():
            return value[:60] + "..." if len(value) > 60 else value
    for value in args.values():
        if isinstance(value, str) and value.strip():
            return value[:60] + "..." if len(value) > 60 else value
    return ""


@dataclass(slots=True)
class ToolcallPreview:
    name: str = ""
    args: str = ""


@dataclass(slots=True)
class AssistantBlock:
    text: str = ""
    thinking: str = ""
    toolcalls: dict[int, ToolcallPreview] = field(default_factory=dict)
    error: str | None = None
    done: bool = False
    usage_text: str = ""

    def has_content(self) -> bool:
        return bool(self.text or self.thinking or self.toolcalls or self.error)

    def append_text(self, delta: str) -> None:
        self.text += delta

    def append_thinking(self, delta: str) -> None:
        self.thinking += delta

    def _ensure_toolcall(self, content_index: int) -> ToolcallPreview:
        preview = self.toolcalls.get(content_index)
        if preview is None:
            preview = ToolcallPreview()
            self.toolcalls[content_index] = preview
        return preview

    def append_toolcall_name(self, content_index: int, delta: str) -> None:
        if not delta:
            return
        self._ensure_toolcall(content_index).name += delta

    def append_toolcall_args(self, content_index: int, delta: str) -> None:
        if not delta:
            return
        self._ensure_toolcall(content_index).args += delta

    def set_toolcall_from_message(self, content_index: int, name: str, args_json: str) -> None:
        self.toolcalls[content_index] = ToolcallPreview(name=name, args=args_json)

    def finish(self) -> None:
        self.done = True

    @staticmethod
    def _single_line_preview(text: str, limit: int = 140) -> str:
        collapsed = " ".join(part for part in text.strip().split())
        if len(collapsed) <= limit:
            return collapsed
        return collapsed[: limit - 3] + "..."

    def render(self) -> RenderableType:
        parts: list[RenderableType] = []

        if self.thinking:
            if self.done:
                parts.append(Text("Thinking...", style="dim italic"))
            else:
                preview = self._single_line_preview(self.thinking, limit=80)
                parts.append(Text(f"Thinking: {preview}", style="dim italic"))

        if self.text:
            if self.done:
                parts.append(Markdown(self.text))
            else:
                parts.append(Text(self.text + "▍"))
        elif not self.done and not self.thinking:
            parts.append(Spinner("dots", text="Thinking..."))

        if self.toolcalls:
            for _index, preview in sorted(self.toolcalls.items())[-2:]:
                name_preview = self._single_line_preview(preview.name, limit=48).strip() or "tool"
                args_preview = self._single_line_preview(preview.args, limit=96).strip()
                tc = Text()
                tc.append("> ", style="cyan")
                tc.append(name_preview, style="bold")
                if args_preview:
                    tc.append(f" ({args_preview})", style="dim")
                parts.append(tc)

        if self.error:
            parts.append(Text(f"Error: {self.error}", style="red"))

        if self.usage_text:
            parts.append(Text(self.usage_text, style="dim"))

        return Group(*parts) if parts else Text("")


@dataclass(slots=True)
class ToolRunBlock:
    tool_call_id: str
    name: str
    args: dict[str, Any]
    status: str = "running"
    is_error: bool = False
    result_summary: str | None = None
    start_time: float = 0.0
    duration: float = 0.0

    def mark_done(self, *, is_error: bool, result_summary: str | None = None) -> None:
        self.status = "done"
        self.is_error = is_error
        self.result_summary = result_summary
        if self.start_time > 0:
            import time
            self.duration = time.time() - self.start_time

    def _key_arg(self) -> str:
        return _extract_tool_key_arg(self.name, self.args)

    def render(self) -> RenderableType:
        key_arg = self._key_arg()

        if self.status == "running":
            label = Text()
            label.append(self.name, style="bold")
            if key_arg:
                label.append(f": {key_arg}", style="dim")
            return Spinner("dots", text=label)

        line = Text()
        if self.is_error:
            line.append("x ", style="red")
        else:
            line.append("✓ ", style="green")
        line.append(self.name, style="bold")
        if key_arg:
            line.append(f": {key_arg}", style="dim")
        if self.duration > 0.1:
            line.append(f" ({self.duration:.2f}s)", style="dim")
        if self.result_summary:
            line.append(f" - {self.result_summary}", style="dim")
        return line


@dataclass(slots=True)
class UserPromptBlock:
    content: str

    def render(self) -> RenderableType:
        t = Text()
        t.append("> ", style="bold cyan")
        t.append(self.content, style="bold")
        return t


@dataclass(slots=True)
class NoticeBlock:
    level: str
    content: str

    def render(self) -> RenderableType:
        style = {"info": "cyan", "warning": "yellow", "error": "red"}.get(self.level, "cyan")
        return Text(self.content, style=style)
