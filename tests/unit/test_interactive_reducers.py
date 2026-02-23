from __future__ import annotations

from gen_agent.interactive.render import InteractiveRenderState, apply_input_history, reduce_session_event
from gen_agent.models.content import TextContent
from gen_agent.models.events import MessageUpdate
from gen_agent.models.messages import AssistantMessage


def test_reduce_message_update_merges_live_on_done() -> None:
    state = InteractiveRenderState()
    assistant = AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text="x")],
        stopReason="stop",
    )

    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "start"}))
    reduce_session_event(
        state,
        MessageUpdate(message=assistant, assistantMessageEvent={"type": "text_delta", "delta": "hello"}),
    )
    reduce_session_event(
        state,
        MessageUpdate(message=assistant, assistantMessageEvent={"type": "thinking_delta", "delta": "plan"}),
    )
    reduce_session_event(
        state,
        MessageUpdate(message=assistant, assistantMessageEvent={"type": "toolcall_delta", "delta": "read"}),
    )
    reduce_session_event(state, MessageUpdate(message=assistant, assistantMessageEvent={"type": "done"}))

    assert state.live.text == ""
    assert state.live.thinking == ""
    assert state.live.toolcall == ""
    assert any("hello" in line for line in state.timeline_lines)
    assert any("plan" in line for line in state.timeline_lines)
    assert any("read" in line for line in state.timeline_lines)


def test_apply_input_history_ignores_empty_and_deduplicates_tail() -> None:
    state = InteractiveRenderState()
    apply_input_history(state, "")
    apply_input_history(state, "first")
    apply_input_history(state, "first")
    apply_input_history(state, "second")

    assert state.input_history == ["first", "second"]
