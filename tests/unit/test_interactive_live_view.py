from __future__ import annotations

import pytest
from rich.console import Console

from gen_agent.interactive.blocks import AssistantBlock, ToolRunBlock
from gen_agent.interactive.live_view import LiveView
from gen_agent.models.content import TextContent
from gen_agent.models.events import AgentStart, MessageUpdate, ToolExecutionEnd, ToolExecutionStart
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
    assert "done output" in rendered


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
    assert "Thinking..." in rendered
    assert ">" in rendered
    assert "read" in rendered
    assert "..." in rendered


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
    assert "read" in rendered
    assert "write" in rendered


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


def test_live_view_commit_prints_done_entries() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message("hello world")

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "text_delta", "delta": "hello world"},
        )
    )

    assert view._committed_count == 0

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "done"}))

    console = Console(record=True, force_terminal=False, width=120)
    view._console = console
    view._live = _FakeLive()
    view._commit_ready_entries()

    assert view._committed_count == 1

    active_entries = view._entries[view._committed_count:]
    assert len(active_entries) == 0
