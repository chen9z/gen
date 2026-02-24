from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Sequence
from typing import Any

from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.rule import Rule
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent
from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage

from .blocks import AssistantBlock, ToolRunBlock, UserPromptBlock

_NOTICE_TTL_SECONDS = {"info": 2.5, "warning": 4.0, "error": 6.0}
_MAX_VISIBLE_NOTICES = 2
_NOTICE_RESERVED_LINES = 1


class LiveView:
    def __init__(
        self,
        session: AgentSession,
        *,
        console: Console | None = None,
        batch_interval: float = 0.04,
        entry_limit: int = 240,
        render_entry_limit: int = 18,
    ) -> None:
        self._session = session
        self._console = console or Console(highlight=False)
        self._batch_interval = batch_interval
        self._entry_limit = entry_limit
        self._render_entry_limit = render_entry_limit

        self._title = "GenInteractive"
        self._header_lines: list[str] = []
        self._footer_lines: list[str] = []
        self._widgets_above: dict[str, list[str]] = {}
        self._widgets_below: dict[str, list[str]] = {}
        self._status_items: dict[str, str] = {}
        self._notices: list[tuple[str, str, float]] = []

        self._entries: list[UserPromptBlock | AssistantBlock | ToolRunBlock] = []
        self._tool_runs: dict[str, ToolRunBlock] = {}
        self._draft: AssistantBlock | None = None
        self._active_toolcall_index: int | None = None
        self._toolcall_phase: dict[int, str] = {}
        self._status_verbose = False
        self._sticky_error_notice: str | None = None
        self._working = False
        self._mooning_spinner: Spinner | None = None

        self._stream_tick = 0
        self._dirty = True

        self._live: Live | None = None
        self._flush_task: asyncio.Task[None] | None = None

    @property
    def stream_tick(self) -> int:
        return self._stream_tick

    @property
    def console(self) -> Console:
        return self._console

    def start(self) -> None:
        if self._live is not None:
            return
        self._live = Live(
            self._build_renderable(),
            console=self._console,
            auto_refresh=False,
            screen=True,
            transient=False,
            vertical_overflow="crop",
            redirect_stdout=False,
            redirect_stderr=False,
        )
        self._live.start()
        self._flush_task = asyncio.create_task(self._flush_loop())
        self.request_refresh(force=True)

    def stop(self) -> None:
        task = self._flush_task
        self._flush_task = None
        if task is not None:
            task.cancel()

        if self._live is not None:
            self._flush_once()
            self._live.stop()
            self._live = None

    def request_refresh(self, *, force: bool = False) -> None:
        self._dirty = True
        if force:
            self._flush_once()

    async def _flush_loop(self) -> None:
        try:
            while True:
                self._flush_once()
                await asyncio.sleep(self._batch_interval)
        except asyncio.CancelledError:
            return

    def _flush_once(self) -> None:
        if self._prune_notices():
            self._dirty = True
        if not self._dirty or self._live is None:
            return
        self._live.update(self._build_renderable(), refresh=True)
        self._dirty = False

    def _prune_notices(self) -> bool:
        if not self._notices:
            return False
        now = time.monotonic()
        kept = [notice for notice in self._notices if notice[2] > now]
        if len(kept) == len(self._notices):
            return False
        self._notices = kept
        return True

    def _active_notices(self) -> list[tuple[str, str]]:
        self._prune_notices()
        active = [(level, text) for level, text, _ in self._notices]
        if self._sticky_error_notice:
            active = [item for item in active if not (item[0] == "error" and item[1] == self._sticky_error_notice)]
            active.append(("error", self._sticky_error_notice))
        return active[-_MAX_VISIBLE_NOTICES:]

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

    def toggle_status_detail(self) -> None:
        self._status_verbose = not self._status_verbose
        self.request_refresh()

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

    def add_notice(self, message: str, *, level: str = "info") -> None:
        ttl = _NOTICE_TTL_SECONDS.get(level, _NOTICE_TTL_SECONDS["info"])
        self._notices.append((level, message, time.monotonic() + ttl))
        self._notices = self._notices[-8:]
        if level == "error":
            self._sticky_error_notice = message
        self.request_refresh()

    def add_user_prompt(self, message: str) -> None:
        self._append_entry(UserPromptBlock(content=message))
        self.request_refresh()

    def add_assistant_message(self, message: AssistantMessage) -> None:
        block = AssistantBlock(done=True)
        self._fill_block_from_message(block, message)
        if not block.has_content() and message.error_message:
            block.error = message.error_message
        self._append_entry(block)
        self.request_refresh()

    def on_session_event(self, event: AgentSessionEvent) -> None:
        etype = getattr(event, "type", "")

        if etype == "agent_start":
            self._working = True
            self._mooning_spinner = Spinner("moon", "")
            self._sticky_error_notice = None
            self.request_refresh()
            return
        if etype == "agent_end":
            self._working = False
            self._mooning_spinner = None
            self.request_refresh()
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
                self.request_refresh()
                return
            if a_type == "thinking_delta":
                self._stream_tick += 1
                self._ensure_draft().append_thinking(delta)
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
            )
            self._tool_runs[event.tool_call_id] = block
            self._append_entry(block)
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
            block.mark_done(
                is_error=bool(getattr(event, "is_error", False)),
                result_summary=self._summarize_tool_result(getattr(event, "result", None)),
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
                f"Retry {event.attempt}/{event.max_attempts} in {event.delay_ms}ms: {event.error_message}",
                level="warning",
            )
            return
        if etype == "auto_retry_end" and not event.success:
            self._clear_mooning_spinner()
            self.add_notice(f"Retry failed: {event.final_error}", level="error")

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

    def _append_entry(self, entry: UserPromptBlock | AssistantBlock | ToolRunBlock) -> None:
        self._entries.append(entry)
        if len(self._entries) <= self._entry_limit:
            return
        removed = self._entries.pop(0)
        if removed is self._draft:
            self._draft = None
        if isinstance(removed, ToolRunBlock):
            self._tool_runs.pop(removed.tool_call_id, None)

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

            start_positions = [pos for marker in ("{", "[") if (pos := delta.find(marker)) >= 0]
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

    def _console_rows(self) -> int:
        try:
            rows = int(getattr(self._console.size, "height", 0) or 0)
        except Exception:
            rows = 0
        return rows if rows > 0 else 24

    def _widget_line_count(self) -> int:
        above = sum(len(lines) for lines in self._widgets_above.values())
        below = sum(len(lines) for lines in self._widgets_below.values())
        return above + below

    def _effective_render_entry_limit(self) -> int:
        rows = self._console_rows()
        reserved = (
            8
            + len(self._header_lines)
            + len(self._footer_lines)
            + _NOTICE_RESERVED_LINES
            + self._widget_line_count()
        )
        return max(6, min(self._entry_limit, rows - reserved))

    def _build_status_line(self) -> Text:
        meta = self._session.get_state()
        provider = meta.get("provider") or "-"
        model = meta.get("modelId") or "-"
        thinking = meta.get("thinkingLevel") or "off"
        session_name = meta.get("sessionName") or "-"
        pending = meta.get("pendingMessageCount", 0)
        status = "Working" if self._working else "Ready"
        if self._status_verbose:
            parts = [
                f"provider={provider}/{model}",
                f"thinking={thinking}",
                f"session={session_name}",
                f"pending={pending}",
                f"status={status}",
            ]
            for key, value in sorted(self._status_items.items()):
                parts.append(f"{key}={value}")
        else:
            parts = [f"{provider}/{model}", f"session={session_name}"]
            if thinking != "off":
                parts.append(f"thinking={thinking}")
            if pending:
                parts.append(f"pending={pending}")
            parts.append(f"status={status}")
        return Text(" | ".join(parts), style="dim")

    def _build_renderable(self) -> RenderableType:
        segments: list[RenderableType] = []
        active_notices = self._active_notices()
        if self._title:
            segments.append(Text(self._title, style="bold"))
        segments.append(self._build_status_line())

        if self._header_lines:
            segments.append(Text(""))
            segments.extend(Text(line, style="bold") for line in self._header_lines)
        for key, lines in sorted(self._widgets_above.items()):
            segments.append(Text(""))
            segments.append(Text(f"{key}", style="magenta"))
            segments.extend(Text(line) for line in lines)

        if self._entries:
            render_limit = self._effective_render_entry_limit()
            start = max(0, len(self._entries) - render_limit)
            renderables: list[RenderableType] = []
            if start > 0:
                renderables.append(Text("... earlier messages omitted ...", style="dim"))

            for item in self._entries[start:]:
                renderables.append(item.render())
                renderables.append(Text(""))
            if renderables and isinstance(renderables[-1], Text) and not renderables[-1].plain:
                renderables.pop()
            content = Group(*renderables)
        else:
            content = Text("Type a message to start...", style="dim")
        segments.append(Text(""))
        segments.append(content)

        if self._mooning_spinner is not None:
            segments.append(Text(""))
            segments.append(self._mooning_spinner)

        if active_notices:
            level, text = active_notices[-1]
            color = {"info": "dim", "warning": "yellow", "error": "red"}.get(level, "dim")
            segments.append(Text(f"* {text}", style=color))
        else:
            segments.append(Text(""))

        if self._footer_lines:
            segments.append(Text(""))
            segments.extend(Text(line, style="dim") for line in self._footer_lines)
        for key, lines in sorted(self._widgets_below.items()):
            segments.append(Text(""))
            segments.append(Text(f"{key}", style="magenta"))
            segments.extend(Text(line) for line in lines)

        segments.append(Rule(style="bright_black"))
        segments.append(Text("Ctrl+C to interrupt", style="dim"))
        return Group(*segments)
