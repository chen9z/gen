from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.text import Text

_FINAL_MARKDOWN_THRESHOLD = 3200


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
        if self.text:
            if self.done:
                if len(self.text) > _FINAL_MARKDOWN_THRESHOLD:
                    parts.append(Text(self.text))
                else:
                    parts.append(Markdown(self.text))
            else:
                parts.append(Text(self.text))
        elif not self.done:
            parts.append(Spinner("dots", text="Gen is thinking..."))

        if self.thinking:
            parts.append(Text(f"thinking: {self._single_line_preview(self.thinking)}", style="dim"))
        if self.toolcalls:
            for _index, preview in sorted(self.toolcalls.items())[-2:]:
                name_preview = self._single_line_preview(preview.name, limit=48).strip() or "tool"
                args_preview = self._single_line_preview(preview.args, limit=96).strip()
                if args_preview:
                    parts.append(Text(f"tool: {name_preview}({args_preview})", style="magenta"))
                else:
                    parts.append(Text(f"tool: {name_preview}", style="magenta"))
        if self.error:
            parts.append(Text(f"Error: {self.error}", style="bold red"))
        return Group(*parts)


@dataclass(slots=True)
class ToolRunBlock:
    tool_call_id: str
    name: str
    args: dict[str, Any]
    status: str = "running"
    is_error: bool = False
    result_summary: str | None = None

    def mark_done(self, *, is_error: bool, result_summary: str | None = None) -> None:
        self.status = "done"
        self.is_error = is_error
        self.result_summary = result_summary

    def _args_summary(self) -> str:
        args_text = json.dumps(self.args, ensure_ascii=False)
        if len(args_text) > 120:
            args_text = args_text[:117] + "..."
        return args_text

    def render(self) -> RenderableType:
        args_text = self._args_summary()
        call = f"{self.name}({args_text})"
        if self.status == "running":
            spinner_text = Text()
            spinner_text.append("● ", style="yellow")
            spinner_text.append(call)
            return Spinner("dots", text=spinner_text)

        style = "red" if self.is_error else "green"
        line = Text()
        line.append("● ", style=style)
        line.append(call)
        if self.result_summary:
            line.append(" · ", style="dim")
            line.append(self.result_summary, style="dim")
        return line


@dataclass(slots=True)
class UserPromptBlock:
    content: str

    def render(self) -> RenderableType:
        return Text(f"> {self.content}", style="bold")


@dataclass(slots=True)
class NoticeBlock:
    level: str
    content: str

    def render(self) -> RenderableType:
        style = {"info": "cyan", "warning": "yellow", "error": "red"}.get(self.level, "cyan")
        return Text(f"[{self.level.upper()}] {self.content}", style=style)
