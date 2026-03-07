from __future__ import annotations

import asyncio

import pytest
from rich.console import Console

from gen_agent.interactive.blocks import AssistantBlock, ToolRunBlock
from gen_agent.interactive.live_view import LiveView
from gen_agent.models.content import TextContent
from gen_agent.models.events import MessageEnd, MessageUpdate, ToolExecutionEnd, ToolExecutionStart
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


def _render_text(view: LiveView) -> str:
    console = Console(record=True, force_terminal=False, width=120)
    console.print(view._build_renderable())
    return console.export_text()


def _emit_text_stream(view: LiveView, message: AssistantMessage, delta: str) -> None:
    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    view.on_session_event(
        MessageUpdate(
            message=message,
            assistantMessageEvent={"type": "text_delta", "delta": delta},
        )
    )
    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "done"}))


def test_live_view_merges_streaming_text_to_assistant_block() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message()
    view.start()
    try:
        _emit_text_stream(view, message, "hello")
    finally:
        view._render_engine.stop()

    assistant_blocks = [entry for entry in view._entries if isinstance(entry, AssistantBlock)]
    assert assistant_blocks
    assert assistant_blocks[-1].text == "hello"
    assert assistant_blocks[-1].done is True


def test_live_view_tracks_tool_start_and_end() -> None:
    view = LiveView(_DummySession())
    view.start()
    try:
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
    finally:
        view._render_engine.stop()

    tool_blocks = [entry for entry in view._entries if isinstance(entry, ToolRunBlock)]
    assert tool_blocks
    assert tool_blocks[-1].status == "done"
    assert tool_blocks[-1].is_error is False

    rendered = _render_text(view)
    assert "Read" in rendered
    assert "README.md" in rendered


def test_live_view_flush_coalesces_when_state_unchanged() -> None:
    view = LiveView(_DummySession())
    fake_live = _FakeLive()
    view._render_engine._live = fake_live

    view.request_refresh()
    view.request_refresh()
    view._flush_once()
    view._flush_once()

    assert fake_live.update_calls == 1


def test_live_view_does_not_start_live_until_content_exists() -> None:
    view = LiveView(_DummySession())
    message = _assistant_message()

    view.start()

    assert not view._render_engine.is_active

    view.on_session_event(MessageUpdate(message=message, assistantMessageEvent={"type": "start"}))
    view._flush_once()

    assert view._render_engine.is_active


def test_live_view_commits_done_entries_during_flush() -> None:
    console = Console(record=True, force_terminal=False, width=120)
    view = LiveView(_DummySession(), console=console)
    message = _assistant_message()
    view._render_engine._live = _FakeLive()

    _emit_text_stream(view, message, "hello")

    view._flush_once()

    assert view._committed_count == 1
    assert "hello" in console.export_text()


def test_live_view_commit_on_stop_prints_entries_and_usage() -> None:
    console = Console(record=True, force_terminal=False, width=120)
    view = LiveView(_DummySession(), console=console)
    message = AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text="done")],
        stopReason="stop",
        usage={"input": 2300, "output": 79, "total_tokens": 2379},
    )

    view.print_user_prompt("hello")
    view.start()
    _emit_text_stream(view, message, "done")
    view.on_session_event(MessageEnd(message=message))
    view.stop()

    rendered = console.export_text()
    assert "hello" in rendered
    assert "done" in rendered
    assert "2.3k input" not in rendered
    assert len(view._entries) == 0
    assert not view._render_engine.is_active


def test_live_view_build_input_toolbar_uses_input_output_and_cache_only() -> None:
    view = LiveView(_DummySession())
    message = AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text="done")],
        stopReason="stop",
        usage={"input": 2300, "output": 79, "cache_read": 512, "total_tokens": 2891},
    )

    view.on_session_event(MessageEnd(message=message))

    assert view.build_input_toolbar() == "2.3k input · 79 output · 512 cache"


def test_live_view_notice_ttl_expires(monkeypatch: pytest.MonkeyPatch) -> None:
    now = {"value": 100.0}
    monkeypatch.setattr("gen_agent.interactive.live_view.time.monotonic", lambda: now["value"])
    view = LiveView(_DummySession())
    view._render_engine._live = _FakeLive()
    view.add_notice("temporary", level="info")

    assert "temporary" in _render_text(view)

    now["value"] += 3.0
    assert "temporary" not in _render_text(view)


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


def test_live_view_renders_title_header_footer_and_status() -> None:
    view = LiveView(_DummySession())
    view.set_title("Build")
    view.set_header(["Header A"])
    view.set_footer(["Footer Z"])
    view.set_status("sync", "ok")

    rendered = _render_text(view)
    assert "Build" in rendered
    assert "Header A" in rendered
    assert "Footer Z" in rendered
    assert "ok" in rendered


@pytest.mark.asyncio
async def test_live_view_flush_loop_updates_live_on_stream_events() -> None:
    view = LiveView(_DummySession(), batch_interval=0.01)
    fake_live = _FakeLive()
    view._render_engine._live = fake_live
    view._min_interval = 0.01
    view._max_interval = 0.02

    loop_task = asyncio.create_task(view._flush_loop())
    try:
        message = _assistant_message()
        _emit_text_stream(view, message, "hello")
        await asyncio.sleep(0.03)
    finally:
        loop_task.cancel()
        await loop_task

    assert fake_live.update_calls >= 1
    assert any(isinstance(entry, AssistantBlock) and entry.text == "hello" for entry in view._entries)


def test_live_view_hides_turn_progress() -> None:
    view = LiveView(_DummySession())
    view._current_turn = 2
    view._max_turns = 30
    view._working = True

    rendered = _render_text(view)
    assert "Turn 2/30" not in rendered
