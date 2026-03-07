from __future__ import annotations

import pytest
from rich.console import Console

from gen_agent.interactive.blocks import AssistantBlock, ToolRunBlock, UserPromptBlock
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
        self.prompts: list[str] = []

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

    async def prompt(self, payload: str):
        self.prompts.append(payload)
        final_message = AssistantMessage(
            provider="openai",
            model="gpt-4o-mini",
            content=[TextContent(text=f"reply:{payload}")],
            stopReason="stop",
        )
        events = [
            AgentStart(),
            MessageUpdate(message=final_message, assistantMessageEvent={"type": "start"}),
            MessageUpdate(
                message=final_message,
                assistantMessageEvent={"type": "text_delta", "delta": "reply:"},
            ),
        ]
        if payload == "hello":
            events.extend(
                [
                    ToolExecutionStart(toolCallId="tc-1", toolName="read", args={"path": "README.md"}),
                    ToolExecutionEnd(
                        toolCallId="tc-1",
                        toolName="read",
                        result={"ok": True},
                        isError=False,
                    ),
                ]
            )
        events.extend(
            [
                MessageUpdate(
                    message=final_message,
                    assistantMessageEvent={"type": "text_delta", "delta": payload},
                ),
                MessageUpdate(message=final_message, assistantMessageEvent={"type": "done"}),
                AgentEnd(messages=[final_message]),
            ]
        )
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
    app._live_view.start()

    ok = await app._submit("hello")

    assert ok is True
    user_blocks = [entry for entry in app._live_view._entries if isinstance(entry, UserPromptBlock)]
    assistant_blocks = [entry for entry in app._live_view._entries if isinstance(entry, AssistantBlock)]
    tool_blocks = [entry for entry in app._live_view._entries if isinstance(entry, ToolRunBlock)]

    assert user_blocks and user_blocks[-1].content == "hello"
    assert assistant_blocks and assistant_blocks[-1].text == "reply:hello"
    assert tool_blocks and tool_blocks[-1].status == "done"
    assert app._live_view._mooning_spinner is None

    console = Console(record=True, force_terminal=False, width=120)
    console.print(app._live_view._build_renderable())
    rendered = console.export_text()
    assert "hello" in rendered
    assert "reply:hello" in rendered
    assert "Calculating" not in rendered
    assert "Ctrl+C to interrupt" not in rendered
    assert "✓ Read" in rendered
    assert "[RUN]" not in rendered
    assert "[OK]" not in rendered
    assert "[ERR]" not in rendered


@pytest.mark.asyncio
async def test_interactive_submit_keeps_persistent_transcript(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = _FakeSession(str(tmp_path))
    app = GenInteractiveApp(session)
    app._session_unsub = session.subscribe(app._on_session_event)
    app._live_view.start()

    first_live = app._live_view._live
    await app._submit("hello")
    await app._submit("again")

    assert app._live_view._live is first_live
    user_blocks = [entry for entry in app._live_view._entries if isinstance(entry, UserPromptBlock)]
    assistant_blocks = [entry for entry in app._live_view._entries if isinstance(entry, AssistantBlock)]
    assert [block.content for block in user_blocks] == ["hello", "again"]
    assert [block.text for block in assistant_blocks][-2:] == ["reply:hello", "reply:again"]

    console = Console(record=True, force_terminal=False, width=120)
    console.print(app._live_view._build_renderable())
    rendered = console.export_text()
    assert rendered.count("reply:") >= 2
