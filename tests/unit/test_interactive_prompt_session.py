from __future__ import annotations

from prompt_toolkit.buffer import Buffer, CompletionState
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document

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


def test_prompt_session_creates_without_error(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )
    assert session is not None


def test_prompt_session_uses_custom_toolbar_provider(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        toolbar_provider=lambda: "custom toolbar",
    )

    assert session._bottom_toolbar().endswith("custom toolbar")


def test_prompt_session_passes_only_bottom_toolbar(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )

    captured = {}

    async def _fake_prompt_async(*args, **kwargs):
        captured.update(kwargs)
        return "ok"

    session._session.prompt_async = _fake_prompt_async

    import asyncio
    result = asyncio.run(session.prompt_async("› "))

    assert result == "ok"
    assert captured["bottom_toolbar"] == session._bottom_toolbar
    assert "rprompt" not in captured


def test_prompt_session_can_clear_last_prompt(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
    )

    calls: list[bool] = []

    class _Renderer:
        def erase(self, *, leave_alternate_screen: bool) -> None:
            calls.append(leave_alternate_screen)

    class _App:
        renderer = _Renderer()

    session._session.app = _App()
    session.clear_last_prompt()

    assert calls == [False]


def test_prompt_session_right_aligns_toolbar_text(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        toolbar_provider=lambda: "2.3k input · 79 output",
    )

    class _Output:
        def get_size(self):
            class _Size:
                columns = 40
            return _Size()

    class _App:
        output = _Output()

    monkeypatch.setattr("gen_agent.interactive.prompt_session.get_app_or_none", lambda: _App())
    toolbar = session._bottom_toolbar()
    assert toolbar.rstrip().endswith("79 output")
    assert len(toolbar) >= len("2.3k input · 79 output")
