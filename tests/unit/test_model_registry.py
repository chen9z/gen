from __future__ import annotations

import json
from pathlib import Path

from gen_agent.core.auth_store import AuthStore
from gen_agent.core.model_registry import ModelRegistry
from gen_agent.models.settings import ApiKeyCredential


def _write_models_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_provider_override_only_applies_to_builtin_models(tmp_path: Path) -> None:
    models_file = tmp_path / "models.json"
    _write_models_json(
        models_file,
        {
            "providers": {
                "openai": {
                    "baseUrl": "https://proxy.openai.local/v1",
                    "headers": {"x-proxy": "openai"},
                }
            }
        },
    )

    registry = ModelRegistry(models_file=models_file)

    openai_model = registry.find_model("openai", "gpt-4o-mini")
    assert openai_model is not None
    assert openai_model.base_url == "https://proxy.openai.local/v1"
    assert openai_model.headers == {"x-proxy": "openai"}

    anthropic_model = registry.find_model("anthropic", "claude-3-5-sonnet-latest")
    assert anthropic_model is not None
    assert anthropic_model.base_url is None


def test_custom_models_upsert_same_id_replace_and_new_id_append(tmp_path: Path) -> None:
    models_file = tmp_path / "models.json"
    _write_models_json(
        models_file,
        {
            "providers": {
                "openai": {
                    "baseUrl": "https://proxy.openai.local/v1",
                    "apiKey": "OPENAI_PROXY_KEY",
                    "api": "openai-completions",
                    "models": [
                        {"id": "gpt-4o-mini", "name": "Proxy Mini", "reasoning": False},
                        {"id": "proxy-only", "name": "Proxy Only", "reasoning": False},
                    ],
                }
            }
        },
    )

    registry = ModelRegistry(models_file=models_file)
    all_models = registry.get_all_models()

    replaced = registry.find_model("openai", "gpt-4o-mini")
    assert replaced is not None
    assert replaced.name == "Proxy Mini"
    assert replaced.base_url == "https://proxy.openai.local/v1"

    assert sum(1 for item in all_models if item.provider == "openai" and item.id == "gpt-4o-mini") == 1
    assert registry.find_model("openai", "proxy-only") is not None
    assert "gpt-4o" in registry.load_catalog()["openai"]


def test_model_overrides_are_partial_and_keep_unspecified_fields(tmp_path: Path) -> None:
    models_file = tmp_path / "models.json"
    _write_models_json(
        models_file,
        {
            "providers": {
                "openai": {
                    "baseUrl": "https://proxy.openai.local/v1",
                    "headers": {"x-provider": "1"},
                    "modelOverrides": {
                        "gpt-4o-mini": {
                            "name": "Mini Override",
                            "cost": {"input": 2.5},
                            "headers": {"x-model": "mini"},
                            "compat": {"routing": {"only": ["a"]}},
                        }
                    },
                }
            }
        },
    )

    registry = ModelRegistry(models_file=models_file)
    model = registry.find_model("openai", "gpt-4o-mini")

    assert model is not None
    assert model.name == "Mini Override"
    assert model.input_cost_per_million == 2.5
    assert model.output_cost_per_million == 0.0
    assert model.context_window == 128000
    assert model.max_tokens == 16384
    assert model.headers == {"x-provider": "1", "x-model": "mini"}
    assert model.compat == {"routing": {"only": ["a"]}}


def test_api_key_precedence_cli_then_auth_then_env_then_models(tmp_path: Path, monkeypatch) -> None:
    models_file = tmp_path / "models.json"
    _write_models_json(
        models_file,
        {
            "providers": {
                "openai": {
                    "baseUrl": "https://proxy.openai.local/v1",
                    "apiKey": "MODEL_KEY",
                }
            }
        },
    )

    auth = AuthStore(path=tmp_path / "auth.json")
    auth.set("openai", ApiKeyCredential(key="AUTH_KEY"))
    monkeypatch.setenv("OPENAI_API_KEY", "ENV_KEY")

    registry = ModelRegistry(auth_store=auth, models_file=models_file)

    assert (
        registry.get_api_key_for_provider("openai", cli_api_key="CLI_KEY", cli_provider="openai")
        == "CLI_KEY"
    )
    assert (
        registry.get_api_key_for_provider("openai", cli_api_key="CLI_KEY", cli_provider="anthropic")
        == "AUTH_KEY"
    )
    assert registry.get_api_key_for_provider("openai") == "AUTH_KEY"

    auth.remove("openai")
    assert registry.get_api_key_for_provider("openai") == "ENV_KEY"

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert registry.get_api_key_for_provider("openai") == "MODEL_KEY"


def test_auth_header_only_applies_to_custom_models(tmp_path: Path) -> None:
    models_file = tmp_path / "models.json"
    _write_models_json(
        models_file,
        {
            "providers": {
                "openai": {
                    "baseUrl": "https://proxy.openai.local/v1",
                    "apiKey": "OPENAI_PROXY_KEY",
                    "api": "openai-completions",
                    "authHeader": True,
                    "models": [{"id": "proxy-model", "name": "Proxy Model"}],
                }
            }
        },
    )

    registry = ModelRegistry(models_file=models_file)

    builtin_model = registry.find_model("openai", "gpt-4o-mini")
    assert builtin_model is not None
    assert not builtin_model.headers or "Authorization" not in builtin_model.headers

    custom_model = registry.find_model("openai", "proxy-model")
    assert custom_model is not None
    assert custom_model.headers is not None
    assert custom_model.headers["Authorization"] == "Bearer OPENAI_PROXY_KEY"
