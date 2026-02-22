from __future__ import annotations

from gen_agent.models.content import TextContent
from gen_agent.models.events import MessageUpdate
from gen_agent.models.messages import AssistantMessage
from gen_agent.tui.reducers import (
    apply_selected_suggestion,
    apply_input_history,
    close_picker,
    focus_next,
    focus_prev,
    history_next,
    history_prev,
    move_picker_selection,
    move_suggestion_selection,
    open_picker,
    reduce_session_event,
    select_picker_by_number,
    selected_suggestion,
    update_command_suggestions,
)
from gen_agent.tui.state import UIState


def test_reduce_message_update_merges_live_on_done() -> None:
    state = UIState()
    assistant = AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text="x")],
        stopReason="stop",
    )

    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "start"}))
    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "text_delta", "delta": "hello"}))
    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "thinking_delta", "delta": "plan"}))
    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "toolcall_delta", "delta": "read"}))
    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "done"}))

    assert state.live.text == ""
    assert state.live.thinking == ""
    assert state.live.toolcall == ""
    assert any("Gen:\nhello" in line for line in state.timeline_lines)
    assert any("Thinking:\nplan" in line for line in state.timeline_lines)
    assert any("Tool call:\nread" in line for line in state.timeline_lines)


def test_picker_state_machine_open_move_select_close() -> None:
    state = UIState()
    items = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    open_picker(state, "tree", items)
    assert state.picker.mode == "tree"
    assert state.focus == "left"

    move_picker_selection(state, 1)
    assert state.picker.selected_index == 1
    move_picker_selection(state, 2)
    assert state.picker.selected_index == 0

    assert select_picker_by_number(state, 2) is True
    assert state.picker.selected_index == 1
    assert select_picker_by_number(state, 9) is False

    close_picker(state)
    assert state.picker.mode is None
    assert state.picker.items == []


def test_focus_cycle_wraps_consistently() -> None:
    state = UIState()
    assert state.focus == "input"
    focus_next(state)
    assert state.focus == "left"
    focus_prev(state)
    assert state.focus == "input"
    focus_prev(state)
    assert state.focus == "right"


def test_input_history_prev_next_roundtrip() -> None:
    state = UIState()
    apply_input_history(state, "first")
    apply_input_history(state, "second")
    assert state.input_history == ["first", "second"]

    assert history_prev(state, "draft") == "second"
    assert history_prev(state, "draft") == "first"
    assert history_next(state) == "second"
    assert history_next(state) == "draft"


def test_command_suggestions_for_slash_prefix() -> None:
    state = UIState()
    update_command_suggestions(state, "/re", ["reload", "resume", "model"])
    assert state.command_suggestions == ["/reload", "/resume"]
    assert selected_suggestion(state) == "/reload"

    move_suggestion_selection(state, 1)
    assert selected_suggestion(state) == "/resume"
    applied = apply_selected_suggestion(state, "/re")
    assert applied == "/resume "

    update_command_suggestions(state, "hello", ["reload"])
    assert state.command_suggestions == []
