from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence
from typing import Any

from rich.console import Console, Group, RenderableType
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage

from .blocks import AssistantBlock, ToolRunBlock, UserPromptBlock
from .commit_manager import CommitManager
from .event_processor import EventProcessor
from .render_engine import RenderEngine
from .state_manager import StateManager

_NOTICE_TTL_SECONDS = {"info": 2.5, "warning": 4.0, "error": 6.0}
_MAX_VISIBLE_NOTICES = 2


class LiveView:
    """Inline scrollback-friendly live view.

    Completed entries are printed to the console (becoming part of terminal
    scrollback).  Only active/streaming entries remain in the Rich Live area.
    """

    def __init__(
        self,
        session: AgentSession,
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

        # Initialize state manager
        self._state = StateManager(entry_limit=entry_limit)

        # Initialize commit manager
        self._commit_manager = CommitManager(self._console)

        # Initialize render engine
        self._render_engine = RenderEngine(self._console, batch_interval)

        # Initialize event processor
        self._event_processor = EventProcessor(self)

        self._stream_tick = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def stream_tick(self) -> int:
        return self._stream_tick

    @property
    def console(self) -> Console:
        return self._console

    # Compatibility properties for state access (delegate to StateManager)
    @property
    def _entries(self) -> list[AssistantBlock | ToolRunBlock]:
        return self._state.get_entries()

    @property
    def _draft(self) -> AssistantBlock | None:
        return self._state.get_draft()

    @_draft.setter
    def _draft(self, value: AssistantBlock | None) -> None:
        self._state.set_draft(value)

    @property
    def _tool_runs(self) -> dict[str, ToolRunBlock]:
        return self._state._tool_runs

    @property
    def _working(self) -> bool:
        return self._state.is_working()

    @_working.setter
    def _working(self, value: bool) -> None:
        self._state.set_working(value)

    @property
    def _sticky_error_notice(self) -> str | None:
        return self._state.get_sticky_error_notice()

    @_sticky_error_notice.setter
    def _sticky_error_notice(self, value: str | None) -> None:
        self._state.set_sticky_error_notice(value)

    @property
    def _mooning_spinner(self) -> Spinner | None:
        return self._state.get_mooning_spinner()

    @_mooning_spinner.setter
    def _mooning_spinner(self, value: Spinner | None) -> None:
        self._state.set_mooning_spinner(value)

    @property
    def _committed_count(self) -> int:
        return self._state.get_committed_count()

    @_committed_count.setter
    def _committed_count(self, value: int) -> None:
        self._state.set_committed_count(value)

    @property
    def _current_usage(self) -> dict[str, Any]:
        return self._state.get_current_usage()

    @property
    def _current_turn(self) -> int:
        return self._state.get_turn_progress()[0]

    @_current_turn.setter
    def _current_turn(self, value: int) -> None:
        _, max_turns = self._state.get_turn_progress()
        self._state.set_turn_progress(value, max_turns)

    @property
    def _max_turns(self) -> int:
        return self._state.get_turn_progress()[1]

    @_max_turns.setter
    def _max_turns(self, value: int) -> None:
        current, _ = self._state.get_turn_progress()
        self._state.set_turn_progress(current, value)

    @property
    def _active_toolcall_index(self) -> int | None:
        return self._state.get_active_toolcall_index()

    @_active_toolcall_index.setter
    def _active_toolcall_index(self, value: int | None) -> None:
        self._state.set_active_toolcall_index(value)

    @property
    def _toolcall_phase(self) -> dict[int, str]:
        return self._state._toolcall_phase

    # Compatibility properties for render engine access
    @property
    def _live(self) -> Live | None:
        return self._render_engine._live

    @_live.setter
    def _live(self, value: Live | None) -> None:
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

    # ------------------------------------------------------------------
    # Welcome banner
    # ------------------------------------------------------------------

    def print_welcome_banner(self) -> None:
        meta = self._session.get_state()
        provider = meta.get("provider") or "-"
        model = meta.get("modelId") or "-"
        session_name = meta.get("sessionName") or "new"
        cwd = self._session.cwd

        self._console.print()
        self._console.print(Panel(
            Group(
                Text(f"  Model:   {provider}/{model}"),
                Text(f"  Session: {session_name}"),
                Text(f"  cwd:     {cwd}", style="dim"),
                Text(),
                Text("  /help for commands, Ctrl+C to interrupt", style="dim"),
            ),
            title="✻ gen-agent",
            title_align="left",
            border_style="dim",
            padding=(0, 0),
        ))
        self._console.print()

    # ------------------------------------------------------------------
    # Direct console output (outside Live)
    # ------------------------------------------------------------------

    def print_prompt_separator(self) -> None:
        width = self._console.width
        self._console.print(Text("─" * width, style="dim"))

    def print_user_prompt(self, message: str) -> None:
        self._console.print()
        self._console.print(UserPromptBlock(content=message).render())

    # ------------------------------------------------------------------
    # Live lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        if self._live is not None:
            return
        self._committed_count = 0
        self._entries.clear()
        self._tool_runs.clear()
        self._draft = None
        self._active_toolcall_index = None
        self._toolcall_phase.clear()
        self._mooning_spinner = None
        self._working = False
        self._notices.clear()
        self._sticky_error_notice = None
        self._state.reset_usage()
        self._last_activity_time = time.monotonic()
        self._stream_tick = 0

        self._live = Live(
            Text(""),
            console=self._console,
            auto_refresh=False,
            transient=False,
            vertical_overflow="visible",
            redirect_stdout=False,
            redirect_stderr=False,
        )
        self._live.start()
        self._flush_task = asyncio.create_task(self._flush_loop())

    def stop(self) -> None:
        task = self._flush_task
        self._flush_task = None
        if task is not None:
            task.cancel()

        if self._live is not None:
            self._commit_ready_entries()
            # Only flush if there are still active (uncommitted) entries,
            # otherwise Live.stop() would write empty content to scrollback
            # causing a visible "page clear" between turns.
            active = self._entries[self._committed_count:]
            if active:
                self._dirty = True
                self._flush_render()
            self._live.update(Text(""), refresh=False)
            self._live.stop()
            self._live = None

    # ------------------------------------------------------------------
    # Refresh helpers
    # ------------------------------------------------------------------

    def request_refresh(self, *, force: bool = False) -> None:
        self._dirty = True
        if force and self._live is not None:
            self._flush_render()

    async def _flush_loop(self) -> None:
        try:
            while True:
                self._flush_once()
                interval = self._calculate_adaptive_interval()
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
        if not self._dirty or self._live is None:
            return
        self._flush_render()

    def _flush_render(self) -> None:
        if self._live is None:
            return
        self._live.update(self._build_renderable(), refresh=True)
        self._dirty = False

    # ------------------------------------------------------------------
    # Commit logic
    # ------------------------------------------------------------------

    def _commit_ready_entries(self) -> None:
        if self._live is None:
            return
        new_count = self._commit_manager.commit_ready_entries(
            self._entries,
            self._committed_count,
        )
        if new_count > self._committed_count:
            self._committed_count = new_count
            self._dirty = True

    # ------------------------------------------------------------------
    # Notices
    # ------------------------------------------------------------------

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
                i for i in active
                if not (i[0] == "error" and i[1] == self._sticky_error_notice)
            ]
            active.append(("error", self._sticky_error_notice))
        return active[-_MAX_VISIBLE_NOTICES:]

    def add_notice(self, message: str, *, level: str = "info") -> None:
        color = {"info": "dim", "warning": "yellow", "error": "red"}.get(level, "dim")
        if self._live is None:
            self._console.print(Text(f"  {message}", style=color))
            return
        ttl = _NOTICE_TTL_SECONDS.get(level, _NOTICE_TTL_SECONDS["info"])
        self._notices.append((level, message, time.monotonic() + ttl))
        self._notices = self._notices[-8:]
        if level == "error":
            self._sticky_error_notice = message
        self.request_refresh()

    # ------------------------------------------------------------------
    # Extension UI passthrough
    # ------------------------------------------------------------------

    def set_title(self, title: str) -> None:
        self.request_refresh()

    def set_header(self, lines: Sequence[str] | None) -> None:
        self.request_refresh()

    def set_footer(self, lines: Sequence[str] | None) -> None:
        self.request_refresh()

    def set_status(self, key: str, text: str | None) -> None:
        if text is None:
            self._status_items.pop(key, None)
        else:
            self._status_items[key] = text
        self.request_refresh()

    def toggle_status_detail(self) -> None:
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

    # ------------------------------------------------------------------
    # Entry management
    # ------------------------------------------------------------------

    def add_user_prompt(self, message: str) -> None:
        self.print_user_prompt(message)

    def add_assistant_message(self, message: AssistantMessage) -> None:
        block = AssistantBlock(done=True)
        self._event_processor._fill_block_from_message(block, message)
        if not block.has_content() and message.error_message:
            block.error = message.error_message
        self._append_entry(block)
        self.request_refresh()

    # ------------------------------------------------------------------
    # Session event handler
    # ------------------------------------------------------------------

    def on_session_event(self, event: AgentSessionEvent) -> None:
        self._event_processor.process(event)

    # ------------------------------------------------------------------
    # Entry helpers
    # ------------------------------------------------------------------

    def _append_entry(self, entry: AssistantBlock | ToolRunBlock) -> None:
        self._entries.append(entry)
        if len(self._entries) <= self._entry_limit:
            return
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

    # ------------------------------------------------------------------
    # Renderable builder
    # ------------------------------------------------------------------

    def _build_renderable(self) -> RenderableType:
        header_parts: list[RenderableType] = []
        main_parts: list[RenderableType] = []
        footer_parts: list[RenderableType] = []

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
            color = {"info": "dim", "warning": "yellow", "error": "red"}.get(level, "dim")
            main_parts.append(Text(f"  {text}", style=color))

        if self._working and self._current_turn > 0 and self._max_turns > 0:
            main_parts.append(Text(f"  Turn {self._current_turn}/{self._max_turns}", style="dim"))

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
