from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from gen_agent.core.auth_store import AuthStore
from gen_agent.core.paths import models_path
from gen_agent.core.resolve_config_value import resolve_config_value, resolve_headers
from gen_agent.models.settings import (
    ModelConfigModel,
    ModelOverride,
    ProviderConfigModel,
    ProviderModelDefinition,
    deep_merge_dict,
)


@dataclass
class RuntimeModel:
    provider: str
    id: str
    name: str
    api: str
    reasoning: bool | None
    input: list[str]
    context_window: int
    max_tokens: int
    input_cost_per_million: float
    output_cost_per_million: float
    cache_read_cost_per_million: float
    cache_write_cost_per_million: float
    base_url: str | None = None
    headers: dict[str, str] | None = None
    compat: dict[str, Any] | None = None

    def to_definition(self) -> ProviderModelDefinition:
        return ProviderModelDefinition.model_validate(
            {
                "id": self.id,
                "name": self.name,
                "api": self.api,
                "reasoning": self.reasoning,
                "input": self.input,
                "contextWindow": self.context_window,
                "maxTokens": self.max_tokens,
                "inputCostPerMillion": self.input_cost_per_million,
                "outputCostPerMillion": self.output_cost_per_million,
                "cacheReadCostPerMillion": self.cache_read_cost_per_million,
                "cacheWriteCostPerMillion": self.cache_write_cost_per_million,
                "headers": self.headers,
                "compat": self.compat,
            }
        )


_BUILTIN_MODELS: list[RuntimeModel] = [
    RuntimeModel(
        provider="openai",
        id="gpt-4o-mini",
        name="gpt-4o-mini",
        api="openai-completions",
        reasoning=None,
        input=["text", "image"],
        context_window=128000,
        max_tokens=16384,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        cache_read_cost_per_million=0.0,
        cache_write_cost_per_million=0.0,
    ),
    RuntimeModel(
        provider="openai",
        id="gpt-4.1-mini",
        name="gpt-4.1-mini",
        api="openai-completions",
        reasoning=None,
        input=["text", "image"],
        context_window=128000,
        max_tokens=16384,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        cache_read_cost_per_million=0.0,
        cache_write_cost_per_million=0.0,
    ),
    RuntimeModel(
        provider="openai",
        id="gpt-4o",
        name="gpt-4o",
        api="openai-completions",
        reasoning=None,
        input=["text", "image"],
        context_window=128000,
        max_tokens=16384,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        cache_read_cost_per_million=0.0,
        cache_write_cost_per_million=0.0,
    ),
    RuntimeModel(
        provider="anthropic",
        id="claude-3-5-sonnet-latest",
        name="claude-3-5-sonnet-latest",
        api="anthropic-messages",
        reasoning=None,
        input=["text", "image"],
        context_window=200000,
        max_tokens=8192,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        cache_read_cost_per_million=0.0,
        cache_write_cost_per_million=0.0,
    ),
    RuntimeModel(
        provider="anthropic",
        id="claude-3-5-haiku-latest",
        name="claude-3-5-haiku-latest",
        api="anthropic-messages",
        reasoning=None,
        input=["text", "image"],
        context_window=200000,
        max_tokens=8192,
        input_cost_per_million=0.0,
        output_cost_per_million=0.0,
        cache_read_cost_per_million=0.0,
        cache_write_cost_per_million=0.0,
    ),
]


class ModelRegistry:
    def __init__(
        self,
        auth_store: AuthStore | None = None,
        models_file: Path | None = None,
    ):
        self.auth_store = auth_store
        self.models_file = models_file or models_path()
        self._models: list[RuntimeModel] = []
        self._provider_configs: dict[str, ProviderConfigModel] = {}
        self._load_error: str | None = None
        self.refresh()

    def refresh(self) -> None:
        self._load_error = None
        builtins = [RuntimeModel(**model.__dict__) for model in _BUILTIN_MODELS]

        config = self._load_model_config()
        if config is None:
            self._models = builtins
            self._provider_configs = {}
            return
        self._provider_configs = dict(config.providers)

        try:
            self._validate_config(config)
        except Exception as exc:
            self._load_error = str(exc)
            self._models = builtins
            self._provider_configs = {}
            return

        builtins = self._apply_provider_overrides(builtins, config)
        custom = self._parse_custom_models(config)
        self._models = self._merge_custom_models(builtins, custom)

    def get_load_error(self) -> str | None:
        return self._load_error

    def get_all_models(self) -> list[RuntimeModel]:
        return [RuntimeModel(**model.__dict__) for model in self._models]

    def find_model(self, provider: str, model_id: str) -> RuntimeModel | None:
        for model in self._models:
            if model.provider == provider and model.id == model_id:
                return RuntimeModel(**model.__dict__)
        return None

    def get_model_definition(self, provider: str, model_id: str) -> ProviderModelDefinition | None:
        model = self.find_model(provider, model_id)
        if not model:
            return None
        return model.to_definition()

    def load_catalog(self) -> dict[str, list[str]]:
        catalog: dict[str, list[str]] = {}
        for model in self._models:
            catalog.setdefault(model.provider, []).append(model.id)
        for provider, ids in list(catalog.items()):
            deduped = list(dict.fromkeys(ids))
            catalog[provider] = deduped
        return catalog

    def resolve_transport_provider(self, provider: str, model_id: str) -> str:
        if provider in {"openai", "anthropic"}:
            return provider
        model = self.find_model(provider, model_id)
        api = model.api if model else None
        if api in {"anthropic-messages"}:
            return "anthropic"
        if api in {"openai-completions", "openai-responses", "openai-chat-completions"}:
            return "openai"
        return provider

    def get_api_key_for_provider(
        self,
        provider: str,
        cli_api_key: str | None = None,
        cli_provider: str | None = None,
    ) -> str | None:
        if cli_api_key and (cli_provider is None or cli_provider == provider):
            return cli_api_key

        cred = self.auth_store.get(provider) if self.auth_store else None
        if cred is not None:
            cred_type = getattr(cred, "type", None)
            if cred_type == "api_key":
                key = resolve_config_value(getattr(cred, "key", ""))
                if key:
                    return key
            if cred_type == "oauth":
                token = getattr(cred, "access_token", None)
                if token:
                    return token

        env_key = _get_env_api_key(provider)
        if env_key:
            return env_key

        provider_cfg = self._provider_configs.get(provider)
        if provider_cfg and provider_cfg.api_key:
            return resolve_config_value(provider_cfg.api_key)
        return None

    def _load_model_config(self) -> ModelConfigModel | None:
        if not self.models_file.exists():
            return ModelConfigModel()
        try:
            raw = json.loads(self.models_file.read_text(encoding="utf-8"))
        except Exception as exc:
            self._load_error = f"Failed to parse models.json: {exc}"
            return None
        try:
            return ModelConfigModel.model_validate(raw)
        except Exception as exc:
            self._load_error = f"Invalid models.json schema: {exc}"
            return None

    def _validate_config(self, config: ModelConfigModel) -> None:
        for provider_name, provider_cfg in config.providers.items():
            has_models = bool(provider_cfg.models)
            has_model_overrides = bool(provider_cfg.model_overrides)

            if not has_models:
                if not provider_cfg.base_url and not has_model_overrides:
                    raise ValueError(
                        f'Provider {provider_name}: must specify "baseUrl", "modelOverrides", or "models".'
                    )
            else:
                if not provider_cfg.base_url:
                    raise ValueError(f'Provider {provider_name}: "baseUrl" is required when defining custom models.')
                if not provider_cfg.api_key:
                    raise ValueError(f'Provider {provider_name}: "apiKey" is required when defining custom models.')

            for model in provider_cfg.models:
                if not model.id:
                    raise ValueError(f"Provider {provider_name}: model missing id")
                if not (provider_cfg.api or model.api):
                    raise ValueError(
                        f'Provider {provider_name}, model {model.id}: no "api" specified. '
                        "Set at provider or model level."
                    )
                if model.context_window is not None and model.context_window <= 0:
                    raise ValueError(f"Provider {provider_name}, model {model.id}: invalid contextWindow")
                if model.max_tokens is not None and model.max_tokens <= 0:
                    raise ValueError(f"Provider {provider_name}, model {model.id}: invalid maxTokens")

    def _apply_provider_overrides(self, builtins: list[RuntimeModel], config: ModelConfigModel) -> list[RuntimeModel]:
        out: list[RuntimeModel] = []
        for model in builtins:
            cfg = config.providers.get(model.provider)
            updated = RuntimeModel(**model.__dict__)
            if cfg:
                provider_headers = resolve_headers(cfg.headers)
                if cfg.base_url:
                    updated.base_url = cfg.base_url
                if provider_headers:
                    updated.headers = {**(updated.headers or {}), **provider_headers}
                override = cfg.model_overrides.get(model.id) if cfg.model_overrides else None
                if override:
                    updated = self._apply_model_override(updated, override)
            out.append(updated)
        return out

    def _apply_model_override(self, model: RuntimeModel, override: ModelOverride) -> RuntimeModel:
        updated = RuntimeModel(**model.__dict__)
        if override.name is not None:
            updated.name = override.name
        if override.reasoning is not None:
            updated.reasoning = override.reasoning
        if override.input is not None:
            updated.input = list(override.input)
        if override.context_window is not None:
            updated.context_window = override.context_window
        if override.max_tokens is not None:
            updated.max_tokens = override.max_tokens
        if override.headers:
            resolved_headers = resolve_headers(override.headers)
            updated.headers = {**(updated.headers or {}), **(resolved_headers or {})}
        if override.compat is not None:
            base_compat = dict(updated.compat or {})
            override_compat = dict(override.compat)
            updated.compat = deep_merge_dict(base_compat, override_compat)
        if override.cost:
            if override.cost.input is not None:
                updated.input_cost_per_million = override.cost.input
            if override.cost.output is not None:
                updated.output_cost_per_million = override.cost.output
            if override.cost.cache_read is not None:
                updated.cache_read_cost_per_million = override.cost.cache_read
            if override.cost.cache_write is not None:
                updated.cache_write_cost_per_million = override.cost.cache_write
        return updated

    def _parse_custom_models(self, config: ModelConfigModel) -> list[RuntimeModel]:
        models: list[RuntimeModel] = []
        for provider_name, provider_cfg in config.providers.items():
            if not provider_cfg.models:
                continue
            provider_headers = resolve_headers(provider_cfg.headers)
            auth_header: dict[str, str] = {}
            if provider_cfg.auth_header and provider_cfg.api_key:
                resolved_key = resolve_config_value(provider_cfg.api_key)
                if resolved_key:
                    auth_header["Authorization"] = f"Bearer {resolved_key}"
            for item in provider_cfg.models:
                item_headers = resolve_headers(item.headers)
                merged_headers = {**(provider_headers or {}), **(item_headers or {}), **auth_header}
                models.append(
                    RuntimeModel(
                        provider=provider_name,
                        id=item.id,
                        name=item.name or item.id,
                        api=item.api or provider_cfg.api or "openai-completions",
                        reasoning=item.reasoning if item.reasoning is not None else False,
                        input=list(item.input or ["text"]),
                        context_window=item.context_window or 128000,
                        max_tokens=item.max_tokens or 16384,
                        input_cost_per_million=item.input_cost_per_million or 0.0,
                        output_cost_per_million=item.output_cost_per_million or 0.0,
                        cache_read_cost_per_million=item.cache_read_cost_per_million or 0.0,
                        cache_write_cost_per_million=item.cache_write_cost_per_million or 0.0,
                        base_url=provider_cfg.base_url,
                        headers=merged_headers or None,
                        compat=item.compat,
                    )
                )
        return models

    def _merge_custom_models(self, builtins: list[RuntimeModel], custom: list[RuntimeModel]) -> list[RuntimeModel]:
        merged = {(model.provider, model.id): model for model in builtins}
        for model in custom:
            merged[(model.provider, model.id)] = model
        ordered: list[RuntimeModel] = []
        seen: set[tuple[str, str]] = set()
        for model in builtins + custom:
            key = (model.provider, model.id)
            if key in seen:
                continue
            seen.add(key)
            ordered.append(merged[key])
        return ordered


def _get_env_api_key(provider: str) -> str | None:
    env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "minimax": "MINIMAX_API_KEY",
        "minimax-cn": "MINIMAX_CN_API_KEY",
    }
    env_name = env_map.get(provider)
    if not env_name:
        return None
    return os.environ.get(env_name)
