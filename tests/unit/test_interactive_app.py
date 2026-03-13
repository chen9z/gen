# tests/unit/test_interactive_app.py
from __future__ import annotations

import asyncio
from contextlib import nullcontext
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from gen_agent.interactive.app import InteractiveApp, _extract_text


class _DummySession:
    def __init__(self) -> None:
        self.provider_name = "openai"
        self.model_id = "gpt-4o-mini"
        self.cwd = "/tmp"
        self._listeners: list = []

    def subscribe(self, listener):
        self._listeners.append(listener)
        return lambda: self._listeners.remove(listener) if listener in self._listeners else None

    async def prompt(self, message, **kwargs):
        return []


class _ErrorSession(_DummySession):
    """Session that raises an exception."""

    async def prompt(self, message, **kwargs):
        raise RuntimeError("API timeout")


def _make_app(session=None) -> InteractiveApp:
    session = session or _DummySession()
    console = Console(file=None, force_terminal=True)
    return InteractiveApp(session, console)


@pytest.mark.asyncio
async def test_run_quit_command():
    app = _make_app()

    class _Prompt:
        calls = 0
        async def prompt_async(self, *a, **kw):
            self.calls += 1
            if self.calls == 1:
                return "/quit"
            raise EOFError

    app._prompt = _Prompt()
    with patch("gen_agent.interactive.app.patch_stdout", return_value=nullcontext()):
        code = await app.run()
    assert code == 0


@pytest.mark.asyncio
async def test_run_help_command(capsys):
    console = Console(force_terminal=False, no_color=True)
    session = _DummySession()
    app = InteractiveApp(session, console)

    class _Prompt:
        calls = 0
        async def prompt_async(self, *a, **kw):
            self.calls += 1
            if self.calls == 1:
                return "/help"
            raise EOFError

    app._prompt = _Prompt()
    with patch("gen_agent.interactive.app.patch_stdout", return_value=nullcontext()):
        await app.run()

    captured = capsys.readouterr()
    assert "/quit" in captured.out
    assert "Ctrl+C" in captured.out


@pytest.mark.asyncio
async def test_run_eof_exits():
    app = _make_app()

    class _Prompt:
        async def prompt_async(self, *a, **kw):
            raise EOFError

    app._prompt = _Prompt()
    with patch("gen_agent.interactive.app.patch_stdout", return_value=nullcontext()):
        code = await app.run()
    assert code == 0


@pytest.mark.asyncio
async def test_run_agent_error_handled():
    app = _make_app(_ErrorSession())
    # _run_agent should catch Exception and not crash
    with patch.object(app, "_console") as mock_console:
        mock_console.print = MagicMock()
        await app._run_agent("hello")
    # Verify error was printed (at least one call should contain "Error")
    calls = [str(c) for c in mock_console.print.call_args_list]
    assert any("Error" in c or "API timeout" in c for c in calls)


@pytest.mark.asyncio
async def test_run_agent_subscribes_and_unsubscribes():
    session = _DummySession()
    app = _make_app(session)
    await app._run_agent("hello")
    # After _run_agent, listener should be unsubscribed
    assert len(session._listeners) == 0


def test_extract_text_from_string():
    class Msg:
        content = "hello world"
    assert _extract_text(Msg()) == "hello world"


def test_extract_text_from_content_blocks():
    class Block:
        type = "text"
        text = "block text"
    class Msg:
        content = [Block()]
    assert _extract_text(Msg()) == "block text"


def test_extract_text_fallback():
    class Msg:
        content = None
    result = _extract_text(Msg())
    assert isinstance(result, str)
