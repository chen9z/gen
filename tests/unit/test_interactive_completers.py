from __future__ import annotations

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document

from gen_agent.interactive.completers import AtPathCompleter, SlashFuzzyCompleter


def test_slash_fuzzy_completer_matches_command_alias() -> None:
    completer = SlashFuzzyCompleter(lambda: ["resume", "reload", "tree"])
    event = CompleteEvent(completion_requested=True)

    completions = list(completer.get_completions(Document("/rsm", 4), event))

    assert any(item.text == "/resume" for item in completions)


def test_at_path_completer_ignores_default_dirs(tmp_path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("x", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print(1)", encoding="utf-8")

    completer = AtPathCompleter(tmp_path)
    paths = completer._get_paths()

    assert "src/main.py" in paths
    assert all(not path.startswith(".git") for path in paths)


def test_at_path_completer_ranks_basename_prefix_first(tmp_path) -> None:
    (tmp_path / "apple.txt").write_text("a", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "maple.md").write_text("b", encoding="utf-8")

    completer = AtPathCompleter(tmp_path)
    event = CompleteEvent(completion_requested=True)
    doc = Document("Read @ap", cursor_position=len("Read @ap"))

    completions = list(completer.get_completions(doc, event))

    assert completions
    assert completions[0].text == "apple.txt"
    assert any(item.text == "docs/maple.md" for item in completions)
