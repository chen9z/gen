"""Minimal streaming view for interactive mode.

Renders agent output via Rich.Live with tool call status.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Literal

from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.models.events import (
    AgentEnd,
    AgentStart,
    AutoCompactionEnd,
    AutoCompactionStart,
    AutoRetryEnd,
    AutoRetryStart,
    MessageUpdate,
    ToolExecutionEnd,
    ToolExecutionStart,
)


@dataclass
class ToolStatus:
    """Minimal tool call tracking."""

    name: str
    args_summary: str = ""
    status: Literal["running", "done", "error"] = "running"
    start_time: float = field(default_factory=time.monotonic)
    duration: float = 0.0
    is_error: bool = False


class StreamView:
    """Streams agent output via Rich.Live."""

    def __init__(self, console: Console) -> None:
        self._console = console
        self._live = Live(console=console, refresh_per_second=10, transient=True)
        self._text_parts: list[str] = []
        self._tools: dict[str, ToolStatus] = {}
        self._working = False
        self._error: str | None = None
        self._notice: str | None = None

    def start(self) -> None:
        self._live.start()

    def stop(self) -> None:
        self._live.stop()

    def on_event(self, event: Any) -> None:
        """Dispatch event to update state, then refresh."""
        if isinstance(event, AgentStart):
            self._working = True
            self._text_parts.clear()
            self._tools.clear()
            self._error = None
            self._notice = None
        elif isinstance(event, MessageUpdate):
            self._on_message_update(event)
        elif isinstance(event, ToolExecutionStart):
            self._tools[event.tool_call_id] = ToolStatus(
                name=event.tool_name,
                args_summary=_summarize_args(event.args),
            )
        elif isinstance(event, ToolExecutionEnd):
            ts = self._tools.get(event.tool_call_id)
            if ts:
                ts.status = "error" if event.is_error else "done"
                ts.duration = time.monotonic() - ts.start_time
                ts.is_error = event.is_error
        elif isinstance(event, AgentEnd):
            self._working = False
        elif isinstance(event, AutoCompactionStart):
            self._notice = "Compacting context..."
        elif isinstance(event, AutoCompactionEnd):
            self._notice = None
        elif isinstance(event, AutoRetryStart):
            self._notice = "Retrying..."
        elif isinstance(event, AutoRetryEnd):
            self._notice = None
        self._refresh()

    def _on_message_update(self, event: MessageUpdate) -> None:
        """Handle streaming text deltas."""
        msg = event.assistant_message_event
        if msg.type == "text_delta" and msg.delta:
            self._text_parts.append(msg.delta)
        elif msg.type == "error" and msg.error:
            self._error = msg.error

    def _refresh(self) -> None:
        """Build renderable group and update Live."""
        parts: list[Any] = []
        text = "".join(self._text_parts)
        if text:
            parts.append(Markdown(text))
        for ts in self._tools.values():
            parts.append(self._render_tool(ts))
        if self._notice:
            parts.append(Text(f"  {self._notice}", style="dim"))
        if self._error:
            parts.append(Text(f"  Error: {self._error}", style="red"))
        if self._working and not self._notice:
            parts.append(Spinner("dots", style="cyan"))
        self._live.update(Group(*parts) if parts else Text(""))

    def _render_tool(self, ts: ToolStatus) -> Text:
        """Render a single tool call status line."""
        if ts.status == "running":
            return Text(f"  \u280b {ts.name} {ts.args_summary} ...", style="yellow")
        icon = "\u2713" if not ts.is_error else "\u2717"
        color = "green" if not ts.is_error else "red"
        return Text(
            f"  {icon} {ts.name} {ts.args_summary} ({ts.duration:.1f}s)",
            style=color,
        )

    def print_final(self, console: Console) -> None:
        """Print completed output to scrollback (Live was transient)."""
        text = "".join(self._text_parts)
        if text:
            console.print(Markdown(text))
        for ts in self._tools.values():
            console.print(self._render_tool(ts))


def _summarize_args(args: dict[str, Any]) -> str:
    """Extract a short summary from tool call arguments."""
    for key in ("path", "file_path", "command", "url", "query", "name"):
        if key in args:
            val = str(args[key])
            return val[:60] + "..." if len(val) > 60 else val
    for val in args.values():
        if isinstance(val, str) and val:
            return val[:40] + "..." if len(val) > 40 else val
    return ""
