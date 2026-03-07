"""Event processor with dispatch table pattern for session events."""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from rich.spinner import Spinner

from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent
from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage

from .blocks import AssistantBlock, ToolRunBlock

if TYPE_CHECKING:
    from .live_view import LiveView


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
    if usage.input > 0:
        parts.append(f"{_format_tokens(usage.input)} input")
    if usage.output > 0:
        parts.append(f"{_format_tokens(usage.output)} output")
    if usage.cache_read > 0:
        parts.append(f"{_format_tokens(usage.cache_read)} cache")
    return " · ".join(parts)


def _truncate_single_line(text: str, limit: int) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: max(0, limit - 3)] + "..."


def _summarize_tool_result(result: Any, limit: int = 96) -> str | None:
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
                        summary = _truncate_single_line(text, limit)
                        return f"error: {summary}" if is_error else summary

        details = result.get("details")
        if details not in (None, "", [], {}):
            if isinstance(details, dict):
                for key in ("brief", "message", "summary", "error", "reason"):
                    value = details.get(key)
                    if isinstance(value, str) and value.strip():
                        summary = _truncate_single_line(value, limit)
                        return f"error: {summary}" if is_error else summary
            try:
                details_text = json.dumps(details, ensure_ascii=False)
            except TypeError:
                details_text = str(details)
            summary = _truncate_single_line(details_text, limit)
            return f"error: {summary}" if is_error else summary

    fallback = _truncate_single_line(str(result), limit)
    return fallback or None


class EventProcessor:
    """Processes session events using a dispatch table."""

    def __init__(self, view: LiveView) -> None:
        self._view = view

        # Top-level event dispatch table
        self._dispatch: dict[str, Callable[[Any], None]] = {
            "agent_start": self._on_agent_start,
            "agent_end": self._on_agent_end,
            "turn_start": self._on_turn_start,
            "message_end": self._on_message_end,
            "message_update": self._on_message_update,
            "tool_execution_start": self._on_tool_start,
            "tool_execution_end": self._on_tool_end,
            "auto_compaction_start": self._on_compaction_start,
            "auto_compaction_end": self._on_compaction_end,
            "auto_retry_start": self._on_retry_start,
            "auto_retry_end": self._on_retry_end,
        }

        # Message update sub-dispatch table
        self._msg_dispatch: dict[str, Callable[[Any, Any, str, int | None], None]] = {
            "start": self._on_msg_start,
            "text_delta": self._on_msg_text_delta,
            "thinking_delta": self._on_msg_thinking_delta,
            "toolcall_start": self._on_msg_toolcall_start,
            "toolcall_delta": self._on_msg_toolcall_delta,
            "toolcall_end": self._on_msg_toolcall_end,
            "error": self._on_msg_error,
            "done": self._on_msg_done,
        }

    def process(self, event: AgentSessionEvent) -> None:
        etype = getattr(event, "type", "")
        handler = self._dispatch.get(etype)
        if handler is not None:
            handler(event)

    # -- Draft / entry helpers (migrated from LiveView) --------------------

    def _start_draft(self) -> None:
        v = self._view
        if v._draft is not None and not v._draft.done:
            v._draft.finish()
        block = AssistantBlock(done=False)
        v._append_entry(block)
        v._draft = block
        v._active_toolcall_index = None
        v._toolcall_phase.clear()
        v.request_refresh()

    def _ensure_draft(self) -> AssistantBlock:
        if self._view._draft is None:
            self._start_draft()
        assert self._view._draft is not None
        return self._view._draft

    def _fill_block_from_message(
        self, block: AssistantBlock, message: AssistantMessage
    ) -> None:
        for item in message.content:
            if isinstance(item, TextContent):
                block.append_text(item.text)
            elif isinstance(item, ThinkingContent):
                block.append_thinking(item.thinking)
            elif isinstance(item, ToolCallContent):
                payload = json.dumps(item.arguments, ensure_ascii=False)
                block.set_toolcall_from_message(len(block.toolcalls), item.name, payload)

    def _clear_mooning_spinner(self) -> None:
        if self._view._mooning_spinner is None:
            return
        self._view._mooning_spinner = None
        self._view.request_refresh()

    def _update_realtime_usage(self, delta: str) -> None:
        if not delta:
            return
        v = self._view
        estimated_tokens = len(delta) // 4
        v._current_usage["output"] += estimated_tokens

    def _append_toolcall_delta(
        self, block: AssistantBlock, content_index: int | None, delta: str
    ) -> None:
        if not delta:
            return
        v = self._view
        index = content_index if isinstance(content_index, int) else v._active_toolcall_index
        if index is None:
            index = -1
        else:
            v._active_toolcall_index = index

        phase = v._toolcall_phase.get(index, "name")
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
                    v._toolcall_phase[index] = "args"
                return

            if stripped.startswith(("{", "[", "\"", ":", ",")):
                block.append_toolcall_args(index, delta)
                v._toolcall_phase[index] = "args"
                return

            block.append_toolcall_name(index, delta)
            v._toolcall_phase.setdefault(index, "name")
            return

        if phase in {"args", "done"}:
            block.append_toolcall_args(index, delta)
            v._toolcall_phase[index] = "args"
            return
        block.append_toolcall_name(index, delta)

    # -- Top-level handlers ------------------------------------------------

    def _on_agent_start(self, event: Any) -> None:
        v = self._view
        v._working = True
        v._mooning_spinner = Spinner("dots", "")
        v._sticky_error_notice = None
        v._current_turn = 0
        v._max_turns = 0
        v.request_refresh()

    def _on_agent_end(self, event: Any) -> None:
        v = self._view
        v._working = False
        v._mooning_spinner = None
        v._sticky_error_notice = None
        v.request_refresh()

    def _on_turn_start(self, event: Any) -> None:
        v = self._view
        v._current_turn = getattr(event, "turn_number", 0)
        v._max_turns = getattr(event, "max_turns", 0)
        v.request_refresh()

    def _on_message_end(self, event: Any) -> None:
        v = self._view
        message = getattr(event, "message", None)
        if isinstance(message, AssistantMessage):
            usage_text = _format_usage(message)
            if usage_text:
                v.set_input_usage_text(usage_text)

    def _on_message_update(self, event: Any) -> None:
        message = getattr(event, "message", None)
        if getattr(message, "role", "") != "assistant":
            return
        self._clear_mooning_spinner()

        assistant_event = getattr(event, "assistant_message_event", None)
        a_type = getattr(assistant_event, "type", "")
        delta = getattr(assistant_event, "delta", "") or ""
        content_index = getattr(assistant_event, "content_index", None)

        handler = self._msg_dispatch.get(a_type)
        if handler is not None:
            handler(message, assistant_event, delta, content_index)

    def _on_tool_start(self, event: Any) -> None:
        v = self._view
        self._clear_mooning_spinner()
        block = ToolRunBlock(
            tool_call_id=event.tool_call_id,
            name=event.tool_name,
            args=event.args,
            start_time=time.time(),
        )
        v._tool_runs[event.tool_call_id] = block
        v._append_entry(block)
        v._last_activity_time = time.monotonic()
        v.request_refresh()

    def _on_tool_end(self, event: Any) -> None:
        v = self._view
        self._clear_mooning_spinner()
        block = v._tool_runs.get(event.tool_call_id)
        if block is None:
            block = ToolRunBlock(
                tool_call_id=event.tool_call_id,
                name=event.tool_name,
                args={},
            )
            v._append_entry(block)
            v._tool_runs[event.tool_call_id] = block
        result = getattr(event, "result", None)
        is_error = bool(getattr(event, "is_error", False))
        block.mark_done(
            is_error=is_error,
            result_summary=_summarize_tool_result(result) if is_error else None,
            error_detail=getattr(event, "error_detail", None),
            result=result,
        )
        v.request_refresh()

    def _on_compaction_start(self, event: Any) -> None:
        self._clear_mooning_spinner()
        self._view.add_notice(f"Auto compact: {event.reason}", level="warning")

    def _on_compaction_end(self, event: Any) -> None:
        self._clear_mooning_spinner()
        self._view.add_notice("Auto compact done", level="info")

    def _on_retry_start(self, event: Any) -> None:
        self._clear_mooning_spinner()
        self._view.add_notice(
            f"Retry {event.attempt}/{event.max_attempts} in {event.delay_ms}ms: "
            f"{event.error_message}",
            level="warning",
        )

    def _on_retry_end(self, event: Any) -> None:
        if not event.success:
            self._clear_mooning_spinner()
            self._view.add_notice(f"Retry failed: {event.final_error}", level="error")

    # -- Message update sub-handlers ---------------------------------------

    def _on_msg_start(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        self._view._stream_tick += 1
        self._start_draft()

    def _on_msg_text_delta(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        self._ensure_draft().append_text(delta)
        self._update_realtime_usage(delta)
        v._last_activity_time = time.monotonic()
        v.request_refresh()

    def _on_msg_thinking_delta(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        self._ensure_draft().append_thinking(delta)
        self._update_realtime_usage(delta)
        v._last_activity_time = time.monotonic()
        v.request_refresh()

    def _on_msg_toolcall_start(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        if isinstance(ci, int):
            v._active_toolcall_index = ci
            v._toolcall_phase[ci] = "name"
        v.request_refresh()

    def _on_msg_toolcall_delta(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        self._append_toolcall_delta(self._ensure_draft(), ci, delta)
        v.request_refresh()

    def _on_msg_toolcall_end(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        if isinstance(ci, int):
            v._toolcall_phase[ci] = "done"
        v.request_refresh()

    def _on_msg_error(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        block = self._ensure_draft()
        block.error = getattr(ae, "error", "") or "provider_error"
        if not block.has_content() and isinstance(message, AssistantMessage):
            self._fill_block_from_message(block, message)
        block.finish()
        v._draft = None
        v._active_toolcall_index = None
        v._toolcall_phase.clear()
        v.request_refresh()

    def _on_msg_done(self, message: Any, ae: Any, delta: str, ci: int | None) -> None:
        v = self._view
        v._stream_tick += 1
        block = self._ensure_draft()
        if not block.has_content() and isinstance(message, AssistantMessage):
            self._fill_block_from_message(block, message)
        block.finish()
        v._draft = None
        v._active_toolcall_index = None
        v._toolcall_phase.clear()
        v.request_refresh()
