from __future__ import annotations

import json

from gen_agent.models.content import Usage, UsageCost
from gen_agent.core.paths import models_path
from gen_agent.models.settings import ModelConfigModel, ProviderModelDefinition


def load_model_config() -> ModelConfigModel:
    path = models_path()
    if not path.exists():
        return ModelConfigModel()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ModelConfigModel()
    try:
        return ModelConfigModel.model_validate(data)
    except Exception:
        return ModelConfigModel()


def load_model_catalog() -> dict[str, list[str]]:
    config = load_model_config()
    catalog: dict[str, list[str]] = {}
    for provider, cfg in config.providers.items():
        ids = [item.id for item in cfg.models if item.id]
        if ids:
            catalog[provider] = ids
    return catalog


def get_model_definition(provider: str, model_id: str) -> ProviderModelDefinition | None:
    config = load_model_config()
    provider_cfg = config.providers.get(provider)
    if not provider_cfg:
        return None
    for model in provider_cfg.models:
        if model.id == model_id:
            return model
    return None


def _cost_for_tokens(tokens: int, price_per_million: float | None) -> float:
    if tokens <= 0 or price_per_million is None:
        return 0.0
    return (tokens / 1_000_000.0) * float(price_per_million)


def compute_usage_cost(provider: str, model_id: str, usage: Usage) -> UsageCost:
    definition = get_model_definition(provider, model_id)
    if definition is None:
        return UsageCost()

    input_cost = _cost_for_tokens(usage.input, definition.input_cost_per_million)
    output_cost = _cost_for_tokens(usage.output, definition.output_cost_per_million)
    cache_read_cost = _cost_for_tokens(usage.cache_read, definition.cache_read_cost_per_million)
    cache_write_cost = _cost_for_tokens(usage.cache_write, definition.cache_write_cost_per_million)
    total = input_cost + output_cost + cache_read_cost + cache_write_cost

    if total == 0.0:
        return UsageCost()

    return UsageCost(
        input=round(input_cost, 10),
        output=round(output_cost, 10),
        cacheRead=round(cache_read_cost, 10),
        cacheWrite=round(cache_write_cost, 10),
        total=round(total, 10),
    )
