from __future__ import annotations

from prompt_toolkit.buffer import Buffer, CompletionState
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document

import pytest

from gen_agent.interactive.prompt_session import (
    InteractivePromptSession,
    accept_completion_or_submit,
    build_input_key_bindings,
    insert_newline,
)


def test_accept_completion_or_submit_prefers_completion() -> None:
    buffer = Buffer()
    buffer.document = Document(text="/res", cursor_position=4)
    completion = Completion(text="/resume", start_position=-4)
    buffer.complete_state = CompletionState(
        original_document=buffer.document,
        completions=[completion],
        complete_index=0,
    )

    accepted = accept_completion_or_submit(buffer)

    assert accepted is True
    assert buffer.text == "/resume"


def test_insert_newline_keeps_existing_content() -> None:
    buffer = Buffer()
    buffer.text = "line-1"
    buffer.cursor_position = len(buffer.text)

    insert_newline(buffer)
    buffer.insert_text("line-2")

    assert buffer.text == "line-1\nline-2"


def test_build_input_key_bindings_includes_multiline_keys() -> None:
    kb = build_input_key_bindings()

    key_sets = {tuple(key.value for key in binding.keys) for binding in kb.bindings}

    assert ("c-j",) in key_sets
    assert ("escape", "c-m") in key_sets
    assert ("c-m",) in key_sets


def test_prompt_session_creates_prompt_toolkit_session(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )

    assert session._session is not None


async def _fake_prompt_async(self, prompt: str, **kwargs):
    _ = self
    return {"prompt": prompt, **kwargs}


@pytest.mark.asyncio
async def test_prompt_session_uses_prompt_async(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )
    monkeypatch.setattr(session._session, "prompt_async", _fake_prompt_async.__get__(session._session))

    result = await session.prompt_async("› ", default="draft")

    assert result["prompt"] == "› "
    assert result["default"] == "draft"
    assert result.get("bottom_toolbar") is None


@pytest.mark.asyncio
async def test_prompt_session_uses_toolbar_provider(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        toolbar_provider=lambda: "usage line",
    )
    monkeypatch.setattr(session._session, "prompt_async", _fake_prompt_async.__get__(session._session))

    result = await session.prompt_async("› ")

    assert callable(result["bottom_toolbar"])
    assert result["bottom_toolbar"]() == "usage line"


def test_prompt_session_records_submission(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )

    session.record_submission("hello")

    assert session._history_store.load()[-1] == "hello"
