from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence
from typing import Any

from rich.console import Console, Group, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage
from gen_agent.runtime import SessionRuntime

from .blocks import AssistantBlock, ToolRunBlock, UserPromptBlock
from .event_processor import EventProcessor
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
        self._entries: list[UserPromptBlock | AssistantBlock | ToolRunBlock] = []
        self._tool_runs: dict[str, ToolRunBlock] = {}
        self._draft: AssistantBlock | None = None
        self._active_toolcall_index: int | None = None
        self._toolcall_phase: dict[int, str] = {}
        self._sticky_error_notice: str | None = None
        self._working = False
        self._mooning_spinner: Spinner | None = None
        self._committed_count = 0
        self._current_usage: dict[str, Any] = {"input": 0, "output": 0, "cost": 0.0}
        self._current_turn = 0
        self._max_turns = 0

        self._render_engine = RenderEngine(self._console, batch_interval)
        self._event_processor = EventProcessor(self)
        self._stream_tick = 0

    @property
    def stream_tick(self) -> int:
        return self._stream_tick

    @property
    def console(self) -> Console:
        return self._console

    @property
    def _live(self):
        return self._render_engine._live

    @_live.setter
    def _live(self, value) -> None:
        self._render_engine._live = value

    @property
    def _flush_task(self) -> asyncio.Task[None] | None:
        return self._render_engine._flush_task

    @_flush_task.setter
    def _flush_task(self, value: asyncio.Task[None] | None) -> None:
        self._render_engine._flush_task = value

    @property
    def _dirty(self) -> bool:
        return self._render_engine._dirty

    @_dirty.setter
    def _dirty(self, value: bool) -> None:
        self._render_engine._dirty = value

    @property
    def _last_activity_time(self) -> float:
        return self._render_engine._last_activity_time

    @_last_activity_time.setter
    def _last_activity_time(self, value: float) -> None:
        self._render_engine._last_activity_time = value

    @property
    def _min_interval(self) -> float:
        return self._render_engine._min_interval

    @property
    def _max_interval(self) -> float:
        return self._render_engine._max_interval

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
        self._entries.clear()
        self._tool_runs.clear()
        self._draft = None
        self._active_toolcall_index = None
        self._toolcall_phase.clear()
        self._mooning_spinner = None
        self._working = False
        self._notices.clear()
        self._sticky_error_notice = None
        self._input_usage_parts = []
        self._reset_usage()
        self._current_turn = 0
        self._max_turns = 0
        self._committed_count = 0
        self._last_activity_time = time.monotonic()
        self._stream_tick = 0
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        self._flush_task = loop.create_task(self._flush_loop()) if loop is not None else None

    def stop(self) -> None:
        self._commit_ready_entries()
        entries = list(self._entries[self._committed_count:])
        notices = self._active_notices()
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
        self._mooning_spinner = None
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
        self._render_engine.request_refresh()
        if force and self._live is not None:
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
        if not self._dirty or self._live is None:
            return
        self._flush_render()

    def _flush_render(self) -> None:
        if self._live is None:
            return
        self._render_engine.flush(self._build_renderable())

    def _has_live_content(self) -> bool:
        if self._title or self._header_lines or self._footer_lines:
            return True
        if self._widgets_above or self._widgets_below:
            return True
        if self._entries[self._committed_count:] or self._mooning_spinner is not None:
            return True
        if self._active_notices():
            return True
        if self._working:
            return True
        if self._status_items:
            return True
        return False

    def _ensure_live_started(self) -> None:
        if self._live is not None or not self._has_live_content():
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
        if self._live is None:
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

    def add_user_prompt(self, message: str) -> None:
        self.print_user_prompt(message)

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

    def build_input_toolbar(self) -> str:
        return " · ".join(self._input_usage_parts)

    def on_session_event(self, event: AgentSessionEvent) -> None:
        self._event_processor.process(event)

    def _append_entry(self, entry: AssistantBlock | ToolRunBlock) -> None:
        self._entries.append(entry)
        while len(self._entries) > self._entry_limit:
            removed = self._entries.pop(0)
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
        header_parts: list[RenderableType] = []
        main_parts: list[RenderableType] = []
        footer_parts: list[RenderableType] = []

        if self._title:
            header_parts.append(Text(f"  {self._title}", style="bold"))
        if self._header_lines:
            header_parts.extend(Text(f"  {line}") for line in self._header_lines)
        for _key, lines in sorted(self._widgets_above.items()):
            header_parts.extend(Text(line) for line in lines)

        active_entries = self._entries[self._committed_count:]
        for entry in active_entries:
            main_parts.append(entry.render())

        if self._mooning_spinner is not None and not active_entries:
            main_parts.append(self._mooning_spinner)

        notices = self._active_notices()
        if notices:
            level, text = notices[-1]
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            footer_parts.append(Text(f"{icon} {text}", style=color))

        if self._status_items:
            status_line = " · ".join(self._status_items.values())
            footer_parts.append(Text(f"  {status_line}", style="dim"))

        if self._footer_lines:
            footer_parts.extend(Text(f"  {line}") for line in self._footer_lines)
        for _key, lines in sorted(self._widgets_below.items()):
            footer_parts.extend(Text(line) for line in lines)
        if self._working:
            footer_parts.append(Text("  Ctrl+C to interrupt", style="dim"))

        has_header = bool(header_parts)
        has_footer = bool(footer_parts)
        has_main = bool(main_parts)
        if not (has_header or has_footer or has_main):
            return Text("")
        if not has_header and not has_footer:
            return Group(*main_parts) if main_parts else Text("")

        layout = Layout()
        sections = []
        if has_header:
            sections.append(Layout(Group(*header_parts), name="header", size=len(header_parts)))
        if has_main:
            sections.append(Layout(Group(*main_parts), name="main"))
        if has_footer:
            sections.append(Layout(Group(*footer_parts), name="footer", size=len(footer_parts)))
        if len(sections) == 1:
            return sections[0].renderable
        layout.split_column(*sections)
        return layout
