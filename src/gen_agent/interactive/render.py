from __future__ import annotations

from dataclasses import dataclass, field

from gen_agent.models.events import AgentSessionEvent

LIVE_CHAR_LIMIT = 8000


@dataclass
class LiveStreamState:
    text: str = ""
    thinking: str = ""
    toolcall: str = ""
    error: str | None = None
    max_chars: int = LIVE_CHAR_LIMIT


@dataclass
class InteractiveRenderState:
    status_text: str = "Ready"
    timeline_lines: list[str] = field(default_factory=list)
    event_lines: list[str] = field(default_factory=list)
    live: LiveStreamState = field(default_factory=LiveStreamState)
    input_history: list[str] = field(default_factory=list)


def _trim_tail(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _append_live_text(state: InteractiveRenderState, target: str, delta: str) -> None:
    if target == "text":
        state.live.text = _trim_tail(state.live.text + delta, state.live.max_chars)
    elif target == "thinking":
        state.live.thinking = _trim_tail(state.live.thinking + delta, state.live.max_chars)
    elif target == "toolcall":
        state.live.toolcall = _trim_tail(state.live.toolcall + delta, state.live.max_chars)


def clear_live(state: InteractiveRenderState) -> None:
    state.live.text = ""
    state.live.thinking = ""
    state.live.toolcall = ""
    state.live.error = None


def merge_live_to_timeline(state: InteractiveRenderState) -> None:
    parts: list[str] = []
    if state.live.text:
        parts.append(state.live.text)
    if state.live.thinking:
        parts.append(f"[thinking]\n{state.live.thinking}")
    if state.live.toolcall:
        parts.append(f"[toolcall]\n{state.live.toolcall}")
    if state.live.error:
        parts.append(f"[error] {state.live.error}")
    if parts:
        state.timeline_lines.append("\n\n".join(parts))
    clear_live(state)


def reduce_session_event(state: InteractiveRenderState, event: AgentSessionEvent) -> None:
    etype = getattr(event, "type", "")
    if etype == "agent_start":
        state.status_text = "Working..."
        return
    if etype == "agent_end":
        state.status_text = "Ready"
        return
    if etype == "message_update":
        message = getattr(event, "message", None)
        if getattr(message, "role", "") != "assistant":
            return
        assistant_event = getattr(event, "assistant_message_event", None)
        event_type = getattr(assistant_event, "type", "")
        delta = getattr(assistant_event, "delta", "") or ""
        if event_type == "start":
            clear_live(state)
            return
        if event_type == "text_delta":
            _append_live_text(state, "text", delta)
            return
        if event_type == "thinking_delta":
            _append_live_text(state, "thinking", delta)
            return
        if event_type == "toolcall_delta":
            _append_live_text(state, "toolcall", delta)
            return
        if event_type == "error":
            state.live.error = getattr(assistant_event, "error", "") or "provider_error"
            merge_live_to_timeline(state)
            return
        if event_type == "done":
            merge_live_to_timeline(state)
            return
        return
    if etype == "tool_execution_start":
        state.event_lines.append(f"Tool start: {event.tool_name} args={event.args}")
        return
    if etype == "tool_execution_end":
        if getattr(event, "is_error", False):
            state.event_lines.append(f"Tool error: {event.tool_name}")
        else:
            state.event_lines.append(f"Tool done: {event.tool_name}")
        return
    if etype == "auto_compaction_start":
        state.event_lines.append(f"Auto compaction start reason={event.reason}")
        return
    if etype == "auto_compaction_end":
        state.event_lines.append("Auto compaction end")
        return
    if etype == "auto_retry_start":
        state.event_lines.append(
            f"Retry attempt={event.attempt}/{event.max_attempts} delay={event.delay_ms}ms error={event.error_message}"
        )
        return
    if etype == "auto_retry_end" and not getattr(event, "success", True):
        state.event_lines.append(f"Retry failed: {event.final_error}")


def apply_input_history(state: InteractiveRenderState, text: str) -> None:
    value = text.strip()
    if not value:
        return
    if not state.input_history or state.input_history[-1] != value:
        state.input_history.append(value)
