from __future__ import annotations

import pytest
from rich.console import Console

from gen_agent.interactive.blocks import AssistantBlock, ToolRunBlock
from gen_agent.interactive.ptk_app import GenInteractiveApp
from gen_agent.models.content import TextContent
from gen_agent.models.events import AgentEnd, AgentStart, MessageUpdate, ToolExecutionEnd, ToolExecutionStart
from gen_agent.models.messages import AssistantMessage


class _Runner:
    def get_commands(self):
        return {}


class _FakeSession:
    def __init__(self, cwd: str) -> None:
        self.cwd = cwd
        self.extension_runner = _Runner()
        self.ui_extensions_enabled = False
        self._listeners = []

    def bind_ui_context(self, _context) -> None:
        return

    def subscribe(self, listener):
        self._listeners.append(listener)

        def _unsub() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return _unsub

    def get_state(self):
        return {
            "provider": "openai",
            "modelId": "gpt-4o-mini",
            "thinkingLevel": "off",
            "sessionName": "demo",
            "pendingMessageCount": 0,
        }

    async def prompt(self, _payload: str):
        final_message = AssistantMessage(
            provider="openai",
            model="gpt-4o-mini",
            content=[TextContent(text="hello")],
            stopReason="stop",
        )
        events = [
            AgentStart(),
            MessageUpdate(message=final_message, assistantMessageEvent={"type": "start"}),
            MessageUpdate(
                message=final_message,
                assistantMessageEvent={"type": "text_delta", "delta": "he"},
            ),
            ToolExecutionStart(toolCallId="tc-1", toolName="read", args={"path": "README.md"}),
            ToolExecutionEnd(
                toolCallId="tc-1",
                toolName="read",
                result={"ok": True},
                isError=False,
            ),
            MessageUpdate(
                message=final_message,
                assistantMessageEvent={"type": "text_delta", "delta": "llo"},
            ),
            MessageUpdate(message=final_message, assistantMessageEvent={"type": "done"}),
            AgentEnd(messages=[final_message]),
        ]
        for listener in list(self._listeners):
            for event in events:
                listener(event)
        return [final_message]


@pytest.mark.asyncio
async def test_interactive_submit_renders_stream_and_tool_blocks(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = _FakeSession(str(tmp_path))
    app = GenInteractiveApp(session)
    app._session_unsub = session.subscribe(app._on_session_event)

    ok = await app._submit("hello")

    assert ok is True
    assistant_blocks = [entry for entry in app._live_view._entries if isinstance(entry, AssistantBlock)]
    tool_blocks = [entry for entry in app._live_view._entries if isinstance(entry, ToolRunBlock)]

    assert assistant_blocks and assistant_blocks[-1].text == "hello"
    assert tool_blocks and tool_blocks[-1].status == "done"
    assert app._live_view._mooning_spinner is None

    console = Console(record=True, force_terminal=False, width=120)
    # Temporarily reset committed count to render all entries for testing
    saved_committed_count = app._live_view._committed_count
    app._live_view._committed_count = 0
    console.print(app._live_view._build_renderable())
    app._live_view._committed_count = saved_committed_count
    rendered = console.export_text()
    assert "Calculating" not in rendered
    assert "Ctrl+C to interrupt" not in rendered  # Not shown after agent finishes
    assert "esc to interrupt" not in rendered.lower()
    assert "✓ Read" in rendered  # Capitalized, no colon
    assert "[RUN]" not in rendered
    assert "[OK]" not in rendered
    assert "[ERR]" not in rendered
