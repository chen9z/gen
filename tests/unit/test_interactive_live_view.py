from __future__ import annotations

import asyncio
import pytest
from rich.console import Console

from gen_agent.interactive.blocks import AssistantBlock, ToolRunBlock, UserPromptBlock
from gen_agent.interactive.live_view import LiveView
from gen_agent.models.content import TextContent
from gen_agent.models.events import AgentStart, MessageEnd, MessageUpdate, ToolExecutionEnd, ToolExecutionStart
from gen_agent.models.messages import AssistantMessage


class _DummySession:
    cwd = "/tmp/test"

    def get_state(self):
        return {
            "provider": "openai",
            "modelId": "gpt-4o-mini",
            "thinkingLevel": "off",
            "sessionName": "demo",
            "pendingMessageCount": 0,
        }


class _FakeLive:
    def __init__(self) -> None:
        self.update_calls = 0

    def update(self, _renderable, refresh=True) -> None:
        _ = refresh
        self.update_calls += 1


def _assistant_message(text: str = "") -> AssistantMessage:
    return AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text=text)] if text else [],
        stopReason="stop",
    )


def test_live_view_merges_streaming_text_to_assistant_block() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message()

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "text_delta", "delta": "hello"},
        )
    )
    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "done"}))

    assistant_blocks = [entry for entry in view._entries if isinstance(entry, AssistantBlock)]
    assert assistant_blocks
    assert assistant_blocks[-1].text == "hello"
    assert assistant_blocks[-1].done is True


def test_live_view_tracks_tool_start_and_end() -> None:
    view = LiveView(_DummySession())

    view.on_session_event(
        ToolExecutionStart(toolCallId="tc-1", toolName="Read", args={"path": "README.md"})
    )
    view.on_session_event(
        ToolExecutionEnd(
            toolCallId="tc-1",
            toolName="Read",
            result={"content": [{"type": "text", "text": "done output"}], "details": {"ok": True}},
            isError=False,
        )
    )

    tool_blocks = [entry for entry in view._entries if isinstance(entry, ToolRunBlock)]
    assert tool_blocks
    assert tool_blocks[-1].status == "done"
    assert tool_blocks[-1].is_error is False

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    rendered = console.export_text()
    assert "Read" in rendered
    assert "README.md" in rendered


def test_live_view_flush_coalesces_when_state_unchanged() -> None:
    view = LiveView(_DummySession())
    fake_live = _FakeLive()
    view._live = fake_live

    view.request_refresh()
    view.request_refresh()
    view._flush_once()
    view._flush_once()

    assert fake_live.update_calls == 1


def test_live_view_removes_calculating_copy_and_uses_moon_spinner() -> None:
    view = LiveView(_DummySession())
    view.on_session_event(AgentStart())

    assert view._mooning_spinner is not None

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    rendered = console.export_text()
    assert "Calculating" not in rendered


def test_live_view_clears_moon_spinner_on_first_assistant_event() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message()
    view.on_session_event(AgentStart())

    assert view._mooning_spinner is not None

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    assert view._mooning_spinner is None


def test_live_view_renders_compact_thinking_and_toolcall_preview() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message()

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "thinking_delta", "delta": "plan " * 80},
        )
    )
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "toolcall_start", "contentIndex": 1},
        )
    )
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "toolcall_delta", "contentIndex": 1, "delta": "read"},
        )
    )
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={
                "type": "toolcall_delta",
                "contentIndex": 1,
                "delta": "{\"path\":\"README.md\",\"mode\":\"r\"}" * 20,
            },
        )
    )
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "toolcall_end", "contentIndex": 1},
        )
    )
    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "done"}))

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    rendered = console.export_text()
    assert "Thinking..." not in rendered
    assert "⏺" not in rendered


def test_live_view_notice_ttl_expires(monkeypatch: pytest.MonkeyPatch) -> None:
    now = {"value": 100.0}
    monkeypatch.setattr("gen_agent.interactive.live_view.time.monotonic", lambda: now["value"])
    view = LiveView(_DummySession())
    view._live = _FakeLive()
    view.add_notice("temporary", level="info")

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    assert "temporary" in console.export_text()

    now["value"] += 3.0
    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    assert "temporary" not in console.export_text()


def test_live_view_handles_interleaved_multi_toolcall_deltas() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message()
    events = [
        {"type": "start"},
        {"type": "toolcall_start", "contentIndex": 1},
        {"type": "toolcall_delta", "contentIndex": 1, "delta": "read"},
        {"type": "toolcall_start", "contentIndex": 2},
        {"type": "toolcall_delta", "contentIndex": 2, "delta": "write"},
        {"type": "toolcall_delta", "contentIndex": 1, "delta": "{\"path\":\"a.txt\"}"},
        {"type": "toolcall_delta", "contentIndex": 2, "delta": "{\"path\":\"b.txt\"}"},
        {"type": "toolcall_end", "contentIndex": 1},
        {"type": "toolcall_end", "contentIndex": 2},
        {"type": "done"},
    ]

    for payload in events:
        view.on_session_event(MessageUpdate(message=message, assistantMessageEvent=payload))

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    rendered = console.export_text()
    assert "⏺" not in rendered


def test_live_view_set_widget_moves_key_between_placements() -> None:
    view = LiveView(_DummySession())
    view.set_widget("summary", ["A"], placement="above_editor")
    assert view._widgets_above["summary"] == ["A"]

    view.set_widget("summary", ["B"], placement="below_editor")
    assert "summary" not in view._widgets_above
    assert view._widgets_below["summary"] == ["B"]

    view.set_widget("summary", None, placement="above_editor")
    assert "summary" not in view._widgets_above
    assert "summary" not in view._widgets_below


def test_live_view_keeps_user_prompt_in_transcript() -> None:
    view = LiveView(_DummySession())
    view.add_user_prompt("hello world")

    assert isinstance(view._entries[-1], UserPromptBlock)

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    rendered = console.export_text()
    assert "hello world" in rendered


def test_live_view_reset_session_view_clears_transcript_but_keeps_widgets() -> None:
    view = LiveView(_DummySession())
    view.add_user_prompt("hello")
    view.set_widget("summary", ["A"], placement="above_editor")
    view.add_notice("temporary", level="info")

    view.reset_session_view()

    assert view._entries == []
    assert view._tool_runs == {}
    assert view._widgets_above["summary"] == ["A"]


def test_live_view_renders_title_header_footer_and_status_detail() -> None:
    view = LiveView(_DummySession())
    view.set_title("Build")
    view.set_header(["Header A"])
    view.set_footer(["Footer Z"])
    view.set_status("sync", "sync=ok")

    compact_console = Console(record=True, force_terminal=False, width=120)
    compact_console.print(view._build_renderable())
    compact = compact_console.export_text()
    assert "Build" in compact
    assert "Header A" in compact
    assert "Footer Z" in compact
    assert "sync=ok" not in compact

    assert view.build_input_toolbar() == ""


@pytest.mark.asyncio
async def test_live_view_flush_loop_updates_live_on_stream_events() -> None:
    view = LiveView(_DummySession(), batch_interval=0.01)
    fake_live = _FakeLive()
    view._live = fake_live
    view._render_engine._min_interval = 0.01
    view._render_engine._max_interval = 0.02

    loop_task = asyncio.create_task(view._flush_loop())
    try:
        message = _assistant_message()
        view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
        view.on_session_event(
            MessageUpdate(
                message=message,
                assistantMessageEvent={"type": "text_delta", "delta": "hello"},
            )
        )
        await asyncio.sleep(0.03)
    finally:
        loop_task.cancel()
        await loop_task

    assert fake_live.update_calls >= 1
    assert any(isinstance(entry, AssistantBlock) and entry.text == "hello" for entry in view._entries)


def test_live_view_hides_turn_progress_until_status_detail() -> None:
    view = LiveView(_DummySession())
    view._current_turn = 2
    view._max_turns = 30
    view._working = True

    compact_console = Console(record=True, force_terminal=False, width=120)
    compact_console.print(view._build_renderable())
    compact = compact_console.export_text()
    assert "turn 2/30" not in compact
    assert view.build_input_toolbar() == ""


def test_live_view_formats_input_usage_toolbar() -> None:
    view = LiveView(_DummySession())
    view.set_input_usage_text("openai/gpt-4o-mini · 2.3k input · 79 output")
    assert view.build_input_toolbar() == "2.3k input · 79 output"


def test_live_view_expands_usage_toolbar_in_detail_mode() -> None:
    view = LiveView(_DummySession())
    view.set_input_usage_text(
        "openai/gpt-4o-mini · 2.3k input · 79 output · 512 cache read · $0.0042"
    )

    assert view.build_input_toolbar() == "2.3k input · 79 output"
    view.toggle_status_detail()
    assert view.build_input_toolbar() == "2.3k input · 79 output · 512 cache read · $0.0042"


def test_live_view_keeps_usage_out_of_assistant_block() -> None:
    view = LiveView(_DummySession())
    message = AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text="done")],
        stopReason="stop",
        usage={"input": 2300, "output": 79, "total_tokens": 2379},
    )

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "text_delta", "delta": "done"},
        )
    )
    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "done"}))
    view.on_session_event(MessageEnd(message=message))

    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    rendered = console.export_text()
    assert "2.3k input" not in rendered
    assert view.build_input_toolbar() == "2.3k input · 79 output"
