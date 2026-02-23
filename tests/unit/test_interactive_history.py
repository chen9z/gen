from __future__ import annotations

from gen_agent.interactive.history import HistoryStore


def test_history_store_isolated_by_cwd(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))

    first = HistoryStore("/tmp/project-a")
    second = HistoryStore("/tmp/project-b")

    assert first.path != second.path
    assert first.path.name.endswith(".jsonl")


def test_history_store_append_load_and_deduplicate(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    cwd = str(tmp_path / "repo")

    store = HistoryStore(cwd)
    store.append("")
    store.append("hello")
    store.append("hello")
    store.append("  world  ")

    loaded = HistoryStore(cwd).load()

    assert loaded == ["hello", "world"]
