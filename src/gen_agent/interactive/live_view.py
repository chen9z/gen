from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Sequence
from typing import Any

from rich.console import Console, Group, RenderableType
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent
from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage

from .blocks import AssistantBlock, ToolRunBlock, UserPromptBlock
from .commit_manager import CommitManager
from .state_manager import StateManager

_NOTICE_TTL_SECONDS = {"info": 2.5, "warning": 4.0, "error": 6.0}
_MAX_VISIBLE_NOTICES = 2


def _format_tokens(n: int) -> str:
    if n <= 0:
        return "0"
    if n < 1000:
        return str(n)
    if n < 10_000:
        return f"{n / 1000:.1f}k"
    return f"{n // 1000}k"


def _format_usage(message: AssistantMessage) -> str:
    usage = message.usage
    if usage.total_tokens <= 0 and usage.input <= 0 and usage.output <= 0:
        return ""
    parts: list[str] = []
    if message.provider or message.model:
        parts.append(f"{message.provider}/{message.model}")
    if usage.input > 0:
        parts.append(f"{_format_tokens(usage.input)} input")
    if usage.output > 0:
        parts.append(f"{_format_tokens(usage.output)} output")
    if usage.cache_read > 0:
        parts.append(f"{_format_tokens(usage.cache_read)} cache read")
    cost = usage.cost.total
    if cost > 0:
        parts.append(f"${cost:.4f}" if cost < 0.01 else f"${cost:.2f}")
    return " · ".join(parts)


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

        self._stream_tick = 0
        self._dirty = True

        self._live: Live | None = None
        self._flush_task: asyncio.Task[None] | None = None

        # Adaptive refresh
        self._last_activity_time = time.monotonic()
        self._min_interval = 0.05  # 20Hz refresh rate (reduced from 50Hz)
        self._max_interval = 0.2

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
            ),
            title="gen-agent",
            title_align="left",
            border_style="bright_black",
            padding=(0, 0),
        ))
        self._console.print(
            Text("  Tips: /help for commands, @ for file paths, Ctrl+C to interrupt",
                 style="dim"),
        )
        self._console.print()

    # ------------------------------------------------------------------
    # Direct console output (outside Live)
    # ------------------------------------------------------------------

    def print_prompt_separator(self) -> None:
        self._console.print(Rule(style="bright_black"))

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
            self._dirty = True
            self._flush_render()
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
        """Calculate adaptive refresh interval based on activity."""
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

    def _update_realtime_usage(self, delta: str) -> None:
        """Update real-time usage estimation during streaming."""
        if not delta:
            return
        # Rough estimation: ~4 chars per token
        estimated_tokens = len(delta) // 4
        self._current_usage["output"] += estimated_tokens
        # Update draft block with estimated usage
        if self._draft and not self._draft.done:
            parts = []
            if self._current_usage["output"] > 0:
                parts.append(f"~{_format_tokens(self._current_usage['output'])} output")
            if parts:
                self._draft.usage_text = " · ".join(parts)

    # ------------------------------------------------------------------
    # Commit logic – print done entries above the Live area
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
    # Extension UI passthrough (kept for API compat)
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
        """Toggle details/diff for the last tool run."""
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
        self._fill_block_from_message(block, message)
        if not block.has_content() and message.error_message:
            block.error = message.error_message
        self._append_entry(block)
        self.request_refresh()

    # ------------------------------------------------------------------
    # Session event handler
    # ------------------------------------------------------------------

    def on_session_event(self, event: AgentSessionEvent) -> None:
        etype = getattr(event, "type", "")

        if etype == "agent_start":
            self._working = True
            self._mooning_spinner = Spinner("dots", "")
            self._sticky_error_notice = None
            self._current_turn = 0
            self._max_turns = 0
            self.request_refresh()
            return
        if etype == "agent_end":
            self._working = False
            self._mooning_spinner = None
            # Clear sticky error on successful completion
            self._sticky_error_notice = None
            self.request_refresh()
            return

        if etype == "turn_start":
            self._current_turn = getattr(event, "turn_number", 0)
            self._max_turns = getattr(event, "max_turns", 0)
            self.request_refresh()
            return

        if etype == "message_end":
            message = getattr(event, "message", None)
            if isinstance(message, AssistantMessage):
                usage_text = _format_usage(message)
                if usage_text:
                    for entry in reversed(self._entries):
                        if isinstance(entry, AssistantBlock):
                            entry.usage_text = usage_text
                            self.request_refresh()
                            break
            return

        if etype == "message_update":
            message = getattr(event, "message", None)
            if getattr(message, "role", "") != "assistant":
                return
            self._clear_mooning_spinner()

            assistant_event = getattr(event, "assistant_message_event", None)
            a_type = getattr(assistant_event, "type", "")
            delta = getattr(assistant_event, "delta", "") or ""
            content_index = getattr(assistant_event, "content_index", None)

            if a_type == "start":
                self._stream_tick += 1
                self._start_draft()
                return
            if a_type == "text_delta":
                self._stream_tick += 1
                self._ensure_draft().append_text(delta)
                self._update_realtime_usage(delta)
                self._last_activity_time = time.monotonic()
                self.request_refresh()
                return
            if a_type == "thinking_delta":
                self._stream_tick += 1
                self._ensure_draft().append_thinking(delta)
                self._update_realtime_usage(delta)
                self._last_activity_time = time.monotonic()
                self.request_refresh()
                return
            if a_type == "toolcall_start":
                self._stream_tick += 1
                if isinstance(content_index, int):
                    self._active_toolcall_index = content_index
                    self._toolcall_phase[content_index] = "name"
                self.request_refresh()
                return
            if a_type == "toolcall_delta":
                self._stream_tick += 1
                self._append_toolcall_delta(self._ensure_draft(), content_index, delta)
                self.request_refresh()
                return
            if a_type == "toolcall_end":
                self._stream_tick += 1
                if isinstance(content_index, int):
                    self._toolcall_phase[content_index] = "done"
                self.request_refresh()
                return
            if a_type == "error":
                self._stream_tick += 1
                block = self._ensure_draft()
                block.error = getattr(assistant_event, "error", "") or "provider_error"
                if not block.has_content() and isinstance(message, AssistantMessage):
                    self._fill_block_from_message(block, message)
                block.finish()
                self._draft = None
                self._active_toolcall_index = None
                # Clean up toolcall phase tracking to prevent memory leaks
                self._toolcall_phase.clear()
                self.request_refresh()
                return
            if a_type == "done":
                self._stream_tick += 1
                block = self._ensure_draft()
                if not block.has_content() and isinstance(message, AssistantMessage):
                    self._fill_block_from_message(block, message)
                block.finish()
                self._draft = None
                self._active_toolcall_index = None
                # Clean up toolcall phase tracking to prevent memory leaks
                self._toolcall_phase.clear()
                self.request_refresh()
                return
            return

        if etype == "tool_execution_start":
            self._clear_mooning_spinner()
            block = ToolRunBlock(
                tool_call_id=event.tool_call_id,
                name=event.tool_name,
                args=event.args,
                start_time=time.time(),
            )
            self._tool_runs[event.tool_call_id] = block
            self._append_entry(block)
            self._last_activity_time = time.monotonic()
            self.request_refresh()
            return

        if etype == "tool_execution_end":
            self._clear_mooning_spinner()
            block = self._tool_runs.get(event.tool_call_id)
            if block is None:
                block = ToolRunBlock(
                    tool_call_id=event.tool_call_id,
                    name=event.tool_name,
                    args={},
                )
                self._append_entry(block)
                self._tool_runs[event.tool_call_id] = block
            result = getattr(event, "result", None)
            block.mark_done(
                is_error=bool(getattr(event, "is_error", False)),
                result_summary=self._summarize_tool_result(result),
                error_detail=getattr(event, "error_detail", None),
                result=result,
            )
            self.request_refresh()
            return

        if etype == "auto_compaction_start":
            self._clear_mooning_spinner()
            self.add_notice(f"Auto compact: {event.reason}", level="warning")
            return
        if etype == "auto_compaction_end":
            self._clear_mooning_spinner()
            self.add_notice("Auto compact done", level="info")
            return
        if etype == "auto_retry_start":
            self._clear_mooning_spinner()
            self.add_notice(
                f"Retry {event.attempt}/{event.max_attempts} in {event.delay_ms}ms: "
                f"{event.error_message}",
                level="warning",
            )
            return
        if etype == "auto_retry_end" and not event.success:
            self._clear_mooning_spinner()
            self.add_notice(f"Retry failed: {event.final_error}", level="error")

    # ------------------------------------------------------------------
    # Draft / entry helpers
    # ------------------------------------------------------------------

    def _start_draft(self) -> None:
        if self._draft is not None and not self._draft.done:
            self._draft.finish()
        block = AssistantBlock(done=False)
        self._append_entry(block)
        self._draft = block
        self._active_toolcall_index = None
        self._toolcall_phase.clear()
        self.request_refresh()

    def _ensure_draft(self) -> AssistantBlock:
        if self._draft is None:
            self._start_draft()
        assert self._draft is not None
        return self._draft

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
            # Clean up all related state for removed tool run
            self._tool_runs.pop(removed.tool_call_id, None)
        elif isinstance(removed, AssistantBlock):
            # Clean up toolcall phase tracking for removed assistant block
            for content_index in list(removed.toolcalls.keys()):
                self._toolcall_phase.pop(content_index, None)

    def _fill_block_from_message(self, block: AssistantBlock, message: AssistantMessage) -> None:
        for item in message.content:
            if isinstance(item, TextContent):
                block.append_text(item.text)
            elif isinstance(item, ThinkingContent):
                block.append_thinking(item.thinking)
            elif isinstance(item, ToolCallContent):
                payload = json.dumps(item.arguments, ensure_ascii=False)
                block.set_toolcall_from_message(len(block.toolcalls), item.name, payload)

    def _clear_mooning_spinner(self) -> None:
        if self._mooning_spinner is None:
            return
        self._mooning_spinner = None
        self.request_refresh()

    def _append_toolcall_delta(
        self, block: AssistantBlock, content_index: int | None, delta: str
    ) -> None:
        if not delta:
            return
        index = content_index if isinstance(content_index, int) else self._active_toolcall_index
        if index is None:
            index = -1
        else:
            self._active_toolcall_index = index

        phase = self._toolcall_phase.get(index, "name")
        stripped = delta.lstrip()
        if phase == "name":
            if stripped in {"(", ")"}:
                return

            start_positions = [
                pos for marker in ("{", "[") if (pos := delta.find(marker)) >= 0
            ]
            boundary = min(start_positions) if start_positions else -1

            if boundary >= 0:
                name_part = delta[:boundary].rstrip(" (")
                args_part = delta[boundary:]
                if name_part:
                    block.append_toolcall_name(index, name_part)
                if args_part:
                    block.append_toolcall_args(index, args_part)
                    self._toolcall_phase[index] = "args"
                return

            if stripped.startswith(("{", "[", "\"", ":", ",")):
                block.append_toolcall_args(index, delta)
                self._toolcall_phase[index] = "args"
                return

            block.append_toolcall_name(index, delta)
            self._toolcall_phase.setdefault(index, "name")
            return

        if phase in {"args", "done"}:
            block.append_toolcall_args(index, delta)
            self._toolcall_phase[index] = "args"
            return
        block.append_toolcall_name(index, delta)

    # ------------------------------------------------------------------
    # Tool result summarisation
    # ------------------------------------------------------------------

    @staticmethod
    def _truncate_single_line(text: str, limit: int) -> str:
        collapsed = " ".join(text.split())
        if len(collapsed) <= limit:
            return collapsed
        return collapsed[: max(0, limit - 3)] + "..."

    def _summarize_tool_result(self, result: Any, limit: int = 96) -> str | None:
        if result is None:
            return None
        if isinstance(result, dict):
            is_error = bool(result.get("isError") or result.get("is_error"))
            content = result.get("content")
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text")
                        if isinstance(text, str) and text.strip():
                            summary = self._truncate_single_line(text, limit)
                            return f"error: {summary}" if is_error else summary

            details = result.get("details")
            if details not in (None, "", [], {}):
                if isinstance(details, dict):
                    for key in ("brief", "message", "summary", "error", "reason"):
                        value = details.get(key)
                        if isinstance(value, str) and value.strip():
                            summary = self._truncate_single_line(value, limit)
                            return f"error: {summary}" if is_error else summary
                try:
                    details_text = json.dumps(details, ensure_ascii=False)
                except TypeError:
                    details_text = str(details)
                summary = self._truncate_single_line(details_text, limit)
                return f"error: {summary}" if is_error else summary

        fallback = self._truncate_single_line(str(result), limit)
        return fallback or None

    # ------------------------------------------------------------------
    # Renderable builder – only uncommitted / active entries
    # ------------------------------------------------------------------

    def _build_renderable(self) -> RenderableType:
        # Build content sections
        header_parts: list[RenderableType] = []
        main_parts: list[RenderableType] = []
        footer_parts: list[RenderableType] = []

        # Header: widgets above
        for _key, lines in sorted(self._widgets_above.items()):
            header_parts.extend(Text(line) for line in lines)

        # Main: active entries
        active_entries = self._entries[self._committed_count:]
        for entry in active_entries:
            main_parts.append(entry.render())

        if self._mooning_spinner is not None and not active_entries:
            main_parts.append(self._mooning_spinner)

        # Main: notices
        notices = self._active_notices()
        if notices:
            level, text = notices[-1]
            color = {"info": "dim", "warning": "yellow", "error": "red"}.get(level, "dim")
            main_parts.append(Text(f"  {text}", style=color))

        # Main: turn progress
        if self._working and self._current_turn > 0 and self._max_turns > 0:
            turn_text = Text(f"  Turn {self._current_turn}/{self._max_turns}", style="dim")
            main_parts.append(turn_text)

        # Footer: widgets below
        for _key, lines in sorted(self._widgets_below.items()):
            footer_parts.extend(Text(line) for line in lines)

        # Footer: keyboard hint
        if self._entries:
            footer_parts.append(Text("  Ctrl+C to interrupt", style="dim"))

        # Use Layout if we have multiple sections, otherwise simple Group
        has_header = bool(header_parts)
        has_footer = bool(footer_parts)
        has_main = bool(main_parts)

        if not (has_header or has_footer or has_main):
            return Text("")

        # Simple case: only main content
        if not has_header and not has_footer:
            return Group(*main_parts) if main_parts else Text("")

        # Use Layout for structured layout
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
