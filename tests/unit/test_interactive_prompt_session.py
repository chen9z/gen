from __future__ import annotations

from prompt_toolkit.buffer import Buffer, CompletionState
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document

import pytest

from gen_agent.interactive.prompt_session import (
    InteractivePromptSession,
    _display_width,
    _fit_toolbar_text,
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
    assert result["wrap_lines"] is False
    assert result["multiline"] is False


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

    assert "bottom_toolbar" not in result
    assert callable(session._session.bottom_toolbar)
    assert session._session.bottom_toolbar().rstrip().endswith("usage line")


def test_prompt_session_hides_toolbar_while_typing(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        toolbar_provider=lambda: "usage line",
    )

    assert callable(session._session.bottom_toolbar)

    session._sync_bottom_toolbar("hello")
    assert session._session.bottom_toolbar is None

    session._sync_bottom_toolbar("")
    assert callable(session._session.bottom_toolbar)


def test_prompt_session_records_submission(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )

    session.record_submission("hello")

    assert session._history_store.load()[-1] == "hello"


def test_prompt_session_formats_toolbar_text_with_right_alignment_and_headroom(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        toolbar_provider=lambda: "2.3k input · 79 output · 512 cache",
    )

    class _Output:
        def get_size(self):
            class _Size:
                columns = 50

            return _Size()

    class _App:
        output = _Output()

    monkeypatch.setattr("gen_agent.interactive.prompt_session.get_app_or_none", lambda: _App())
    toolbar = session._bottom_toolbar()

    assert toolbar.rstrip().endswith("512 cache")
    assert _display_width(toolbar) <= 49
    assert _fit_toolbar_text("2.3k input · 79 output · 512 cache", 20).endswith("12 cache")
