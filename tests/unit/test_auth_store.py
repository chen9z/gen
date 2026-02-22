from pathlib import Path

from gen_agent.core.auth_store import AuthStore
from gen_agent.models.settings import ApiKeyCredential


def test_auth_store_precedence_cli_over_env_over_file(tmp_path: Path, monkeypatch) -> None:
    auth_file = tmp_path / "auth.json"
    store = AuthStore(path=auth_file)
    store.set("openai", ApiKeyCredential(key="file-key"))
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")

    assert store.get_api_key("openai", cli_api_key="cli-key") == "cli-key"
    assert store.get_api_key("openai") == "env-key"

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert store.get_api_key("openai") == "file-key"


def test_auth_store_cli_key_scoped_to_cli_provider(tmp_path: Path, monkeypatch) -> None:
    auth_file = tmp_path / "auth.json"
    store = AuthStore(path=auth_file)
    store.set("anthropic", ApiKeyCredential(key="file-anthropic"))
    monkeypatch.setenv("OPENAI_API_KEY", "env-openai")

    assert store.get_api_key("openai", cli_api_key="cli-openai", cli_provider="openai") == "cli-openai"
    assert store.get_api_key("anthropic", cli_api_key="cli-openai", cli_provider="openai") == "file-anthropic"


def test_auth_store_reads_legacy_provider_map_shape(tmp_path: Path) -> None:
    auth_file = tmp_path / "auth.json"
    auth_file.write_text('{"openai":{"type":"api_key","key":"legacy-key"}}', encoding="utf-8")

    store = AuthStore(path=auth_file)
    assert store.get_api_key("openai") == "legacy-key"
