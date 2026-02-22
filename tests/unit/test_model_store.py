from pathlib import Path

import pytest

from gen_agent.core.model_store import compute_usage_cost, load_model_catalog
from gen_agent.models.content import Usage


def test_load_model_catalog_from_models_json(tmp_path: Path, monkeypatch) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"openai":{"baseUrl":"https://proxy.openai.local/v1","apiKey":"OPENAI_PROXY_KEY","api":"openai-completions","models":[{"id":"gpt-4.1-mini"},{"id":"gpt-4o-mini"}]},'
            '"custom":{"baseUrl":"https://custom.local/v1","apiKey":"CUSTOM_KEY","api":"openai-completions","models":[{"id":"my-model"}]}'
            "}"
            "}"
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))

    catalog = load_model_catalog()
    assert "gpt-4.1-mini" in catalog["openai"]
    assert "gpt-4o-mini" in catalog["openai"]
    assert "gpt-4o" in catalog["openai"]
    assert catalog["custom"] == ["my-model"]


def test_models_json_ignores_extra_fields_and_computes_cost(tmp_path: Path, monkeypatch) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"openai":{"unusedProviderField":"x","models":[{'
            '"id":"gpt-4o-mini",'
            '"api":"openai-completions",'
            '"unknownField":"keep-compatible",'
            '"pricing":{"inputCostPerM":2.0,"outputCostPerM":8.0,"cacheReadCostPerM":1.0,"cacheWriteCostPerM":4.0}'
            '}],"baseUrl":"https://proxy.openai.local/v1","apiKey":"OPENAI_PROXY_KEY"}'
            '},'
            '"extraTopLevel":"ok"'
            "}"
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))

    catalog = load_model_catalog()
    assert "gpt-4o-mini" in catalog["openai"]

    usage = Usage(input=1_000_000, output=500_000, cacheRead=250_000, cacheWrite=125_000, totalTokens=1_500_000)
    cost = compute_usage_cost("openai", "gpt-4o-mini", usage)
    assert cost.input == pytest.approx(2.0)
    assert cost.output == pytest.approx(4.0)
    assert cost.cache_read == pytest.approx(0.25)
    assert cost.cache_write == pytest.approx(0.5)
    assert cost.total == pytest.approx(6.75)


def test_compute_usage_cost_defaults_to_zero_without_pricing(tmp_path: Path, monkeypatch) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"openai":{"baseUrl":"https://proxy.openai.local/v1","apiKey":"OPENAI_PROXY_KEY","api":"openai-completions","models":[{"id":"gpt-4o-mini"}]}'
            "}"
            "}"
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))

    usage = Usage(input=1000, output=1000, totalTokens=2000)
    cost = compute_usage_cost("openai", "gpt-4o-mini", usage)
    assert cost.total == 0.0
