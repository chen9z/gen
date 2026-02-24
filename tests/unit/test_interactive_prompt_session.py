from __future__ import annotations

from prompt_toolkit.buffer import Buffer, CompletionState
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text
from wcwidth import wcswidth

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


def test_prompt_session_toolbar_uses_short_hint(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        status_provider=lambda: "",
    )

    fragments = to_formatted_text(session._bottom_toolbar())
    rendered = "".join(text for _style, text, *_ in fragments)
    assert "Enter send" in rendered
    assert "Esc+Enter newline" in rendered
    assert "Ctrl+C interrupt" in rendered


def test_prompt_session_toolbar_truncates_on_narrow_width(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        status_provider=lambda: "",
    )
    monkeypatch.setattr(session, "_toolbar_columns", lambda: 56)

    fragments = to_formatted_text(session._bottom_toolbar())
    rendered = "".join(text for _style, text, *_ in fragments)
    assert len(rendered.strip()) <= 56
    assert "Enter send" in rendered
    assert "Ctrl+C interrupt" in rendered


def test_prompt_session_truncate_respects_display_width(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    session = InteractivePromptSession(
        cwd=str(tmp_path),
        command_provider=lambda: [],
        status_provider=lambda: "",
    )

    clipped = session._truncate_with_ellipsis("宽宽宽宽宽宽宽宽宽宽", 8)
    assert wcswidth(clipped) <= 8
    assert clipped.endswith("...")
