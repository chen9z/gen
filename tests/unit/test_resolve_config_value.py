from __future__ import annotations

import shlex
from pathlib import Path

from gen_agent.core.resolve_config_value import clear_config_value_cache, resolve_config_value, resolve_headers


def test_resolve_config_value_prefers_env(monkeypatch) -> None:
    monkeypatch.setenv("MY_API_KEY", "env-secret")
    assert resolve_config_value("MY_API_KEY") == "env-secret"


def test_resolve_config_value_falls_back_to_literal(monkeypatch) -> None:
    monkeypatch.delenv("literal-token", raising=False)
    assert resolve_config_value("literal-token") == "literal-token"


def test_resolve_config_value_command_is_cached(tmp_path: Path) -> None:
    clear_config_value_cache()
    marker = tmp_path / "marker.txt"
    marker_quoted = shlex.quote(str(marker))
    command = f"!sh -c 'echo run >> {marker_quoted}; echo token'"

    assert resolve_config_value(command) == "token"
    assert resolve_config_value(command) == "token"
    assert marker.read_text(encoding="utf-8").splitlines() == ["run"]


def test_resolve_headers_drops_empty_values(monkeypatch) -> None:
    monkeypatch.setenv("X_TOKEN", "abc")
    resolved = resolve_headers({"x-token": "X_TOKEN", "x-empty": "!false"})
    assert resolved == {"x-token": "abc"}
