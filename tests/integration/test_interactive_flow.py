from __future__ import annotations

import pytest
from rich.console import Console

from gen_agent.interactive.ptk_app import GenInteractiveApp
from gen_agent.models.content import TextContent
from gen_agent.models.events import AgentEnd, AgentStart, MessageEnd, MessageUpdate, ToolExecutionEnd, ToolExecutionStart
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
            usage={"input": 2300, "output": 79, "total_tokens": 2379},
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
                MessageEnd(message=final_message),
                AgentEnd(messages=[final_message]),
            ]
        )
        for listener in list(self._listeners):
            for event in events:
                listener(event)
        return [final_message]


@pytest.mark.asyncio
async def test_interactive_submit_writes_final_output_to_scrollback(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = _FakeSession(str(tmp_path))
    app = GenInteractiveApp(session)
    console = Console(record=True, force_terminal=False, width=120)
    app._live_view = app._live_view.__class__(session, console=console)
    app._session_unsub = session.subscribe(app._on_session_event)

    ok = await app._submit("hello")

    assert ok is True
    rendered = console.export_text()
    assert rendered.count("› hello") == 1
    assert "reply:hello" in rendered
    assert "✓ Read README.md" in rendered
    assert rendered.count("reply:hello") == 1
    assert rendered.count("✓ Read README.md") == 1
    assert "2.3k input · 79 output" not in rendered
    assert app._live_view._entries == []
    assert not app._live_view._render_engine.is_active
    assert app._live_view.build_input_toolbar() == "2.3k input · 79 output"


@pytest.mark.asyncio
async def test_interactive_submit_keeps_scrollback_between_turns(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = _FakeSession(str(tmp_path))
    app = GenInteractiveApp(session)
    console = Console(record=True, force_terminal=False, width=120)
    app._live_view = app._live_view.__class__(session, console=console)
    app._session_unsub = session.subscribe(app._on_session_event)

    await app._submit("hello")
    await app._submit("again")

    rendered = console.export_text()
    assert rendered.count("reply:") >= 2
    assert "reply:hello" in rendered
    assert "reply:again" in rendered
