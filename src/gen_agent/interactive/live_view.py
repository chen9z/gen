from __future__ import annotations

import asyncio
import time
from collections import deque
from collections.abc import Sequence
from typing import Any

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage
from gen_agent.runtime import SessionRuntime

from .blocks import AssistantBlock, ToolRunBlock, UserPromptBlock
from .event_processor import EventProcessor, format_tokens
from .render_engine import RenderEngine

_NOTICE_TTL_SECONDS = {"info": 2.5, "warning": 4.0, "error": 6.0}
_MAX_VISIBLE_NOTICES = 2
_NOTICE_ICONS = {"info": "ℹ", "warning": "⚠", "error": "✗"}
_NOTICE_COLORS = {"info": "dim", "warning": "yellow", "error": "red"}


class LiveView:
    """Current-turn transient live view with scrollback commits."""

    def __init__(
        self,
        session: SessionRuntime,
        *,
        console: Console | None = None,
        batch_interval: float = 0.04,
        entry_limit: int = 240,
    ) -> None:
        self._session = session
        self._console = console or Console(highlight=False)
        self._batch_interval = batch_interval
        self._entry_limit = entry_limit

        self._widgets_above: dict[str, list[str]] = {}
        self._widgets_below: dict[str, list[str]] = {}
        self._status_items: dict[str, str] = {}
        self._notices: list[tuple[str, str, float]] = []
        self._header_lines: list[str] = []
        self._footer_lines: list[str] = []
        self._title: str | None = None
        self._input_usage_parts: list[str] = []

        # Inlined from StateManager
        self._entries: deque[UserPromptBlock | AssistantBlock | ToolRunBlock] = deque()
        self._tool_runs: dict[str, ToolRunBlock] = {}
        self._draft: AssistantBlock | None = None
        self._active_toolcall_index: int | None = None
        self._toolcall_phase: dict[int, str] = {}
        self._sticky_error_notice: str | None = None
        self._working = False
        self._idle_spinner: Spinner | None = None
        self._committed_count = 0
        self._current_usage: dict[str, Any] = {"input": 0, "output": 0, "cost": 0.0}
        self._current_turn = 0
        self._max_turns = 0

        self._render_engine = RenderEngine(self._console)
        self._dirty = True
        self._last_activity_time = 0.0
        self._flush_task: asyncio.Task[None] | None = None
        self._min_interval = 0.05
        self._max_interval = 0.2
        self._event_processor = EventProcessor(self)
        self._stream_tick = 0

    @property
    def stream_tick(self) -> int:
        return self._stream_tick

    @property
    def console(self) -> Console:
        return self._console

    # -- Usage helpers (inlined from StateManager) -------------------------

    def _update_usage(self, input_tokens: int = 0, output_tokens: int = 0, cost: float = 0.0) -> None:
        self._current_usage["input"] += input_tokens
        self._current_usage["output"] += output_tokens
        self._current_usage["cost"] += cost

    def _reset_usage(self) -> None:
        self._current_usage = {"input": 0, "output": 0, "cost": 0.0}

    # -- Public API --------------------------------------------------------

    def print_welcome_banner(self) -> None:
        self._console.print(self.build_welcome_renderable())

    def build_welcome_renderable(self) -> RenderableType:
        meta = self._session.get_state()
        provider = meta.get("provider") or "-"
        model = meta.get("modelId") or "-"
        session_name = meta.get("sessionName") or "new"
        cwd = self._session.cwd
        return Panel(
            Group(
                Text(f"  Model:   {provider}/{model}"),
                Text(f"  Session: {session_name}"),
                Text(f"  cwd:     {cwd}", style="dim"),
                Text("  /help for commands, Ctrl+C to interrupt", style="dim"),
            ),
            title="✻ gen-agent",
            title_align="left",
            border_style="dim",
            padding=(0, 0),
        )

    def print_user_prompt(self, message: str) -> None:
        self._console.print(UserPromptBlock(content=message).render())

    def start(self) -> None:
        if self._flush_task is not None:
            return
        self._reset_turn_state(clear_usage=True)
        self._last_activity_time = time.monotonic()
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        self._flush_task = loop.create_task(self._flush_loop()) if loop is not None else None

    def stop(self) -> None:
        self._commit_ready_entries()
        entries = list(self._entries)[self._committed_count:]
        notices = self._active_notices()
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None
        self._render_engine.stop()
        self._commit_entries(entries, notices)
        self._reset_turn_state(clear_usage=False)

    def reset_session_view(self) -> None:
        self._reset_turn_state(clear_usage=True)

    def _reset_turn_state(self, *, clear_usage: bool) -> None:
        self._entries.clear()
        self._tool_runs.clear()
        self._draft = None
        self._active_toolcall_index = None
        self._toolcall_phase.clear()
        self._idle_spinner = None
        self._working = False
        self._sticky_error_notice = None
        self._notices.clear()
        if clear_usage:
            self._input_usage_parts = []
        self._reset_usage()
        self._current_turn = 0
        self._max_turns = 0
        self._committed_count = 0
        self._stream_tick = 0
        self._dirty = False

    def request_refresh(self, *, force: bool = False) -> None:
        self._dirty = True
        self._last_activity_time = time.monotonic()
        if force and self._render_engine.is_active:
            self._flush_render()

    async def _flush_loop(self) -> None:
        try:
            while True:
                self._flush_once()
                if self._dirty:
                    interval = self._calculate_adaptive_interval()
                else:
                    interval = self._batch_interval
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            return

    def _calculate_adaptive_interval(self) -> float:
        if self._working:
            return self._min_interval
        time_since = time.monotonic() - self._last_activity_time
        idle_factor = min(time_since / 2.0, 5.0)
        return min(self._max_interval, self._batch_interval * (1 + idle_factor))

    def _flush_once(self) -> None:
        self._commit_ready_entries()
        if self._prune_notices():
            self._dirty = True
        self._ensure_live_started()
        if not self._dirty or not self._render_engine.is_active:
            return
        self._flush_render()

    def _flush_render(self) -> None:
        if not self._render_engine.is_active:
            return
        self._render_engine.flush(self._build_renderable())
        self._dirty = False

    def _has_live_content(self) -> bool:
        if self._title or self._header_lines or self._footer_lines:
            return True
        if self._widgets_above or self._widgets_below:
            return True
        if self._committed_count < len(self._entries) or self._idle_spinner is not None:
            return True
        if self._active_notices():
            return True
        if self._working:
            return True
        if self._status_items:
            return True
        return False

    def _ensure_live_started(self) -> None:
        if self._render_engine.is_active or not self._has_live_content():
            return
        self._render_engine.start()

    def _prune_notices(self) -> bool:
        if not self._notices:
            return False
        now = time.monotonic()
        kept = [n for n in self._notices if n[2] > now]
        if len(kept) == len(self._notices):
            return False
        self._notices = kept
        return True

    def _active_notices(self) -> list[tuple[str, str]]:
        self._prune_notices()
        active = [(level, text) for level, text, _ in self._notices]
        if self._sticky_error_notice:
            active = [
                item for item in active
                if not (item[0] == "error" and item[1] == self._sticky_error_notice)
            ]
            active.append(("error", self._sticky_error_notice))
        return active[-_MAX_VISIBLE_NOTICES:]

    def add_notice(self, message: str, *, level: str = "info") -> None:
        icon = _NOTICE_ICONS.get(level, "ℹ")
        color = _NOTICE_COLORS.get(level, "dim")
        if not self._render_engine.is_active:
            self._console.print(Text(f"{icon} {message}", style=color))
            return
        ttl = _NOTICE_TTL_SECONDS.get(level, _NOTICE_TTL_SECONDS["info"])
        self._notices.append((level, message, time.monotonic() + ttl))
        self._notices = self._notices[-8:]
        if level == "error":
            self._sticky_error_notice = message
        self.request_refresh()

    def set_title(self, title: str) -> None:
        self._title = title
        self.request_refresh()

    def set_header(self, lines: Sequence[str] | None) -> None:
        self._header_lines = list(lines or [])
        self.request_refresh()

    def set_footer(self, lines: Sequence[str] | None) -> None:
        self._footer_lines = list(lines or [])
        self.request_refresh()

    def set_status(self, key: str, text: str | None) -> None:
        if text is None:
            self._status_items.pop(key, None)
        else:
            self._status_items[key] = text
        self.request_refresh()

    def toggle_last_tool_details(self) -> None:
        for entry in reversed(self._entries):
            if isinstance(entry, ToolRunBlock):
                if entry.is_error and entry.error_detail:
                    entry.toggle_details()
                elif not entry.is_error and entry.result:
                    entry.toggle_diff()
                self.request_refresh()
                break

    def toggle_last_thinking(self) -> None:
        for entry in reversed(self._entries):
            if isinstance(entry, AssistantBlock) and entry.thinking:
                entry.toggle_thinking()
                self.request_refresh()
                break

    def set_widget(self, key: str, lines: Sequence[str] | None, *, placement: str) -> None:
        if placement == "below_editor":
            target = self._widgets_below
            other = self._widgets_above
        else:
            target = self._widgets_above
            other = self._widgets_below
        other.pop(key, None)
        if lines is None:
            target.pop(key, None)
        else:
            target[key] = list(lines)
        self.request_refresh()

    def add_assistant_message(self, message: AssistantMessage) -> None:
        block = AssistantBlock(done=True)
        self._event_processor._fill_block_from_message(block, message)
        if not block.has_content() and message.error_message:
            block.error = message.error_message
        self._append_entry(block)
        self.request_refresh()

    def set_input_usage_text(self, usage_text: str) -> None:
        self._input_usage_parts = [part.strip() for part in usage_text.split(" · ") if part.strip()]
        self.request_refresh()

    def clear_input_usage_text(self) -> None:
        self._input_usage_parts = []
        self.request_refresh()

    def clear_interrupt_state(self) -> None:
        """Clear tool-call phase tracking on interrupt."""
        self._toolcall_phase.clear()

    def build_input_toolbar(self) -> str:
        return " · ".join(self._input_usage_parts)

    def on_session_event(self, event: AgentSessionEvent) -> None:
        self._event_processor.process(event)

    def _append_entry(self, entry: AssistantBlock | ToolRunBlock) -> None:
        self._entries.append(entry)
        while len(self._entries) > self._entry_limit:
            removed = self._entries.popleft()
            if self._committed_count > 0:
                self._committed_count -= 1
            if removed is self._draft:
                self._draft = None
            if isinstance(removed, ToolRunBlock):
                self._tool_runs.pop(removed.tool_call_id, None)
            elif isinstance(removed, AssistantBlock):
                for content_index in list(removed.toolcalls.keys()):
                    self._toolcall_phase.pop(content_index, None)
        self._last_activity_time = time.monotonic()

    def _commit_ready_entries(self) -> None:
        if self._committed_count >= len(self._entries):
            return
        new_committed = self._committed_count
        for index in range(self._committed_count, len(self._entries)):
            entry = self._entries[index]
            if isinstance(entry, AssistantBlock) and entry.done:
                self._console.print(entry.render())
                new_committed = index + 1
                continue
            if isinstance(entry, ToolRunBlock) and entry.status == "done":
                self._console.print(entry.render())
                new_committed = index + 1
                continue
            break
        if new_committed > self._committed_count:
            self._committed_count = new_committed
            self._dirty = True

    def _commit_entries(
        self,
        entries: Sequence[AssistantBlock | ToolRunBlock],
        notices: Sequence[tuple[str, str]],
    ) -> None:
        for entry in entries:
            self._console.print(entry.render())
        for level, text in notices:
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            self._console.print(Text(f"{icon} {text}", style=color))

    def _build_renderable(self) -> RenderableType:
        parts: list[RenderableType] = []

        if self._title:
            parts.append(Text(f"  {self._title}", style="bold"))
        if self._header_lines:
            parts.extend(Text(f"  {line}") for line in self._header_lines)
        for _key, lines in sorted(self._widgets_above.items()):
            parts.extend(Text(line) for line in lines)

        active_entries = list(self._entries)[self._committed_count:]
        for entry in active_entries:
            parts.append(entry.render())

        if self._idle_spinner is not None and not active_entries:
            parts.append(self._idle_spinner)

        for level, text in self._active_notices():
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            parts.append(Text(f"{icon} {text}", style=color))

        # Real-time usage + turn progress (CC-style status line)
        status_parts: list[str] = []
        if self._working:
            usage = self._current_usage
            if usage["output"] > 0:
                status_parts.append(f"~{format_tokens(usage['output'])} output")
            if self._current_turn > 0:
                turn_text = f"turn {self._current_turn}"
                if self._max_turns > 0:
                    turn_text += f"/{self._max_turns}"
                status_parts.append(turn_text)
        if self._status_items:
            status_parts.extend(self._status_items.values())
        if status_parts:
            parts.append(Text(f"  {' · '.join(status_parts)}", style="dim"))

        if self._footer_lines:
            parts.extend(Text(f"  {line}") for line in self._footer_lines)
        for _key, lines in sorted(self._widgets_below.items()):
            parts.extend(Text(line) for line in lines)
        if self._working:
            parts.append(Text("  Ctrl+C to interrupt", style="dim"))

        return Group(*parts) if parts else Text("")
