from __future__ import annotations

from typing import Iterable

from .state import PaneFocus, PickerMode, UIState

_FOCUS_ORDER: list[PaneFocus] = ["left", "center", "right", "input"]


def _trim_tail(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _append_live_text(state: UIState, target: str, delta: str) -> None:
    if target == "text":
        state.live.text = _trim_tail(state.live.text + delta, state.live.max_chars)
    elif target == "thinking":
        state.live.thinking = _trim_tail(state.live.thinking + delta, state.live.max_chars)
    elif target == "toolcall":
        state.live.toolcall = _trim_tail(state.live.toolcall + delta, state.live.max_chars)


def clear_live(state: UIState) -> None:
    state.live.text = ""
    state.live.thinking = ""
    state.live.toolcall = ""
    state.live.error = None


def _merge_live_to_timeline(state: UIState) -> None:
    parts: list[str] = []
    if state.live.text:
        parts.append(f"Gen:\n{state.live.text}")
    if state.live.thinking:
        parts.append(f"Thinking:\n{state.live.thinking}")
    if state.live.toolcall:
        parts.append(f"Tool call:\n{state.live.toolcall}")
    if state.live.error:
        parts.append(f"[error] {state.live.error}")
    if parts:
        state.timeline_lines.append("\n\n".join(parts))
    clear_live(state)


def reduce_session_event(state: UIState, event) -> None:
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
            _merge_live_to_timeline(state)
            return
        if event_type == "done":
            _merge_live_to_timeline(state)
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


def focus_next(state: UIState) -> None:
    idx = _FOCUS_ORDER.index(state.focus)
    state.focus = _FOCUS_ORDER[(idx + 1) % len(_FOCUS_ORDER)]


def focus_prev(state: UIState) -> None:
    idx = _FOCUS_ORDER.index(state.focus)
    state.focus = _FOCUS_ORDER[(idx - 1) % len(_FOCUS_ORDER)]


def open_picker(state: UIState, mode: PickerMode, items: list[dict]) -> None:
    state.picker.mode = mode
    state.picker.items = list(items)
    state.picker.selected_index = 0
    state.focus = "left"


def close_picker(state: UIState) -> None:
    state.picker.mode = None
    state.picker.items = []
    state.picker.selected_index = 0
    clear_live(state)


def move_picker_selection(state: UIState, delta: int) -> None:
    if not state.picker.is_open or not state.picker.items:
        return
    total = len(state.picker.items)
    state.picker.selected_index = (state.picker.selected_index + delta) % total


def page_picker_selection(state: UIState, delta_pages: int, page_size: int = 10) -> None:
    move_picker_selection(state, delta_pages * page_size)


def select_picker_by_number(state: UIState, number: int) -> bool:
    if not state.picker.is_open:
        return False
    index = number - 1
    if index < 0 or index >= len(state.picker.items):
        return False
    state.picker.selected_index = index
    return True


def apply_input_history(state: UIState, text: str) -> None:
    value = text.strip()
    if not value:
        state.history_cursor = None
        state.history_draft = ""
        return
    if not state.input_history or state.input_history[-1] != value:
        state.input_history.append(value)
    state.history_cursor = None
    state.history_draft = ""


def history_prev(state: UIState, current_input: str) -> str:
    if not state.input_history:
        return current_input
    if state.history_cursor is None:
        state.history_draft = current_input
        state.history_cursor = len(state.input_history) - 1
    else:
        state.history_cursor = max(0, state.history_cursor - 1)
    return state.input_history[state.history_cursor]


def history_next(state: UIState) -> str:
    if state.history_cursor is None:
        return state.history_draft
    if state.history_cursor >= len(state.input_history) - 1:
        state.history_cursor = None
        return state.history_draft
    state.history_cursor += 1
    return state.input_history[state.history_cursor]


def update_command_suggestions(state: UIState, text: str, commands: Iterable[str]) -> None:
    if not text.startswith("/"):
        state.command_suggestions = []
        state.selection.suggestion_index = 0
        return
    token = text[1:].strip()
    candidates = sorted(f"/{cmd}" for cmd in commands if cmd.startswith(token))
    state.command_suggestions = candidates[:12]
    state.selection.suggestion_index = 0


def move_suggestion_selection(state: UIState, delta: int) -> None:
    if not state.command_suggestions:
        return
    total = len(state.command_suggestions)
    state.selection.suggestion_index = (state.selection.suggestion_index + delta) % total


def selected_suggestion(state: UIState) -> str | None:
    if not state.command_suggestions:
        return None
    idx = state.selection.suggestion_index
    if idx < 0 or idx >= len(state.command_suggestions):
        return state.command_suggestions[0]
    return state.command_suggestions[idx]


def apply_selected_suggestion(state: UIState, current_input: str) -> str:
    suggestion = selected_suggestion(state)
    if suggestion is None:
        return current_input
    if " " in current_input.strip():
        first, _, rest = current_input.strip().partition(" ")
        if first.startswith("/"):
            return f"{suggestion} {rest}".rstrip() + " "
    return f"{suggestion} "
