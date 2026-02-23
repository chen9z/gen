from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.text import Text


@dataclass(slots=True)
class AssistantBlock:
    text: str = ""
    thinking: str = ""
    toolcall: str = ""
    error: str | None = None
    done: bool = False

    def has_content(self) -> bool:
        return bool(self.text or self.thinking or self.toolcall or self.error)

    def append_text(self, delta: str) -> None:
        self.text += delta

    def append_thinking(self, delta: str) -> None:
        self.thinking += delta

    def append_toolcall(self, delta: str) -> None:
        self.toolcall += delta

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
                parts.append(Markdown(self.text))
            else:
                parts.append(Text(self.text))
        elif not self.done:
            parts.append(Spinner("dots", text="Gen is thinking..."))

        if self.thinking:
            parts.append(Text(f"thinking: {self._single_line_preview(self.thinking)}", style="dim"))
        if self.toolcall:
            parts.append(Text(f"tool: {self._single_line_preview(self.toolcall)}", style="magenta"))
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

    def mark_done(self, *, is_error: bool) -> None:
        self.status = "done"
        self.is_error = is_error

    def _args_summary(self) -> str:
        args_text = json.dumps(self.args, ensure_ascii=False)
        if len(args_text) > 120:
            args_text = args_text[:117] + "..."
        return args_text

    def render(self) -> RenderableType:
        args_text = self._args_summary()
        call = f"{self.name}({args_text})"
        if self.status == "running":
            return Spinner("dots", text=f"[RUN] {call}")

        if self.is_error:
            return Text(f"[ERR] {call}", style="red")
        return Text(f"[OK] {call}", style="green")


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
