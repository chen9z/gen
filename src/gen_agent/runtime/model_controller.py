from __future__ import annotations

import re
from fnmatch import fnmatch
from typing import TYPE_CHECKING

from gen_agent.core.settings_store import save_settings

if TYPE_CHECKING:
    from gen_agent.core.model_registry import ModelRegistry
    from gen_agent.core.session_manager import SessionManager
    from gen_agent.models.settings import SettingsModel


VALID_THINKING_LEVELS = {"off", "minimal", "low", "medium", "high", "xhigh"}


class ModelController:
    def __init__(
        self,
        *,
        cwd: str,
        model_registry: "ModelRegistry",
        session_manager: "SessionManager",
        settings: "SettingsModel",
        project_settings: "SettingsModel",
        provider: str | None,
        model: str | None,
        thinking_level: str | None,
        cli_api_key: str | None,
        cli_api_key_provider: str | None,
    ) -> None:
        self._cwd = cwd
        self._model_registry = model_registry
        self._session_manager = session_manager
        self._settings = settings
        self._project_settings = project_settings
        self._cli_api_key = cli_api_key
        self._cli_api_key_provider = cli_api_key_provider
        self._scoped_model_patterns: list[str] = list(settings.enabled_models)
        self._last_model_scope_warnings: list[str] = []

        parsed_model, model_thinking = self.split_model_thinking(model)
        provider_name, model_id = self.resolve_provider_and_model(provider, parsed_model)
        self.provider_name = provider_name
        self.model_id = model_id
        self.thinking_level = thinking_level or model_thinking or settings.default_thinking_level or "off"
        self._clamp_thinking_for_current_model()

    @property
    def scoped_model_patterns(self) -> list[str]:
        return list(self._scoped_model_patterns)

    @property
    def last_scope_warnings(self) -> list[str]:
        return list(self._last_model_scope_warnings)

    def update_settings(self, settings: "SettingsModel", project_settings: "SettingsModel") -> None:
        self._settings = settings
        self._project_settings = project_settings
        self._scoped_model_patterns = list(project_settings.enabled_models)
        self._clamp_thinking_for_current_model()

    def set_cli_provider_scope(self, provider: str | None) -> None:
        self._cli_api_key_provider = provider

    def split_model_thinking(self, model: str | None) -> tuple[str | None, str | None]:
        if not model or ":" not in model:
            return model, None
        candidate_model, candidate_level = model.rsplit(":", 1)
        if candidate_level in VALID_THINKING_LEVELS and candidate_model:
            return candidate_model, candidate_level
        return model, None

    def resolve_provider_and_model(self, provider: str | None, model: str | None) -> tuple[str, str]:
        catalog = self._available_model_catalog()
        all_models = [(p, m) for p, models in catalog.items() for m in models]

        explicit_provider = provider
        model_pattern = model
        if model and "/" in model and not provider:
            pfx, model_id = model.split("/", 1)
            if pfx in catalog:
                explicit_provider = pfx
                model_pattern = model_id
            else:
                return pfx, model_id

        if explicit_provider:
            provider_name = explicit_provider
        elif self._settings.default_provider and self._settings.default_provider in catalog:
            provider_name = self._settings.default_provider
        elif "openai" in catalog:
            provider_name = "openai"
        else:
            provider_name = next(iter(catalog), "openai")

        if model_pattern:
            candidates = [(provider_name, item) for item in catalog.get(provider_name, [])] if explicit_provider else all_models
            resolved = self._resolve_model_pattern(model_pattern, candidates)
            if resolved:
                return resolved[0]
            return provider_name, model_pattern

        if self._settings.default_model:
            resolved = self._resolve_model_pattern(self._settings.default_model, all_models)
            if resolved:
                return resolved[0]

        provider_models = catalog.get(provider_name, [])
        if provider_models:
            return provider_name, provider_models[0]
        if all_models:
            return all_models[0]
        return provider_name, self._settings.default_model or "gpt-4o-mini"

    def set_model(self, provider: str, model_id: str) -> None:
        self.provider_name = provider
        self.model_id = model_id
        self._session_manager.append_model_change(provider, model_id)
        self.set_thinking_level(self.thinking_level)

    def set_model_from_text(self, text: str) -> str:
        if not text:
            return f"Current model: {self.provider_name}/{self.model_id}"
        model_value, thinking = self.split_model_thinking(text)
        provider_name, model_id = self.resolve_provider_and_model(None, model_value)
        self.provider_name = provider_name
        self.model_id = model_id
        self._session_manager.append_model_change(provider_name, model_id)
        if thinking:
            self.set_thinking_level(thinking)
        else:
            self._clamp_thinking_for_current_model()
        return f"Model set to {self.provider_name}/{self.model_id}"

    def set_thinking_level(self, level: str) -> None:
        if level not in VALID_THINKING_LEVELS:
            raise ValueError("invalid thinking level")
        effective = level if self._model_supports_reasoning(self.provider_name, self.model_id) else "off"
        if effective == self.thinking_level:
            return
        self.thinking_level = effective
        self._session_manager.append_thinking_level(effective)

    def sync_from_session_context(self) -> None:
        if not self._session_manager.entries:
            return
        context = self._session_manager.build_context()
        model = context.model
        if model and model.get("provider") and model.get("modelId"):
            self.provider_name = str(model["provider"])
            self.model_id = str(model["modelId"])
        if context.thinking_level:
            self.thinking_level = context.thinking_level
        self._clamp_thinking_for_current_model()

    def set_scoped_models(self, patterns: list[str]) -> list[str]:
        cleaned = [item.strip() for item in patterns if item.strip()]
        self._scoped_model_patterns = cleaned
        self._project_settings.enabled_models = cleaned
        save_settings(self._cwd, self._project_settings, scope="project")
        resolved_models, warnings = self._resolve_scoped_models_with_warnings()
        self._last_model_scope_warnings = warnings
        out: list[str] = []
        for provider, model, thinking in resolved_models:
            token = f"{provider}/{model}"
            if thinking:
                token += f":{thinking}"
            out.append(token)
        return out

    def apply_scoped_startup_model(self) -> bool:
        scoped = self._prefer_models_with_auth(self._resolve_scoped_models())
        if not scoped:
            return False
        current = (self.provider_name, self.model_id)
        pairs = [(provider, model) for provider, model, _thinking in scoped]
        if current in pairs:
            scoped_thinking = scoped[pairs.index(current)][2]
            if scoped_thinking:
                self.thinking_level = scoped_thinking
            self._clamp_thinking_for_current_model()
            return False
        self.provider_name, self.model_id, scoped_thinking = scoped[0]
        if scoped_thinking:
            self.thinking_level = scoped_thinking
        self._clamp_thinking_for_current_model()
        return True

    def cycle_model(self, direction: str = "forward") -> dict[str, str | bool]:
        scoped = self._prefer_models_with_auth(self._resolve_scoped_models())
        if not scoped:
            scoped = [(self.provider_name, self.model_id, None)]
        current = (self.provider_name, self.model_id)
        pairs = [(provider, model) for provider, model, _thinking in scoped]
        step = -1 if direction == "backward" else 1
        if current not in pairs:
            self.provider_name, self.model_id, scoped_thinking = scoped[0]
        else:
            idx = (pairs.index(current) + step) % len(scoped)
            self.provider_name, self.model_id, scoped_thinking = scoped[idx]
        self._session_manager.append_model_change(self.provider_name, self.model_id)
        if scoped_thinking:
            self.set_thinking_level(scoped_thinking)
        else:
            self.set_thinking_level(self.thinking_level)
        return {
            "provider": self.provider_name,
            "modelId": self.model_id,
            "thinkingLevel": self.thinking_level,
            "isScoped": bool(self._scoped_model_patterns),
        }

    def _available_model_catalog(self) -> dict[str, list[str]]:
        self._model_registry.refresh()
        return self._model_registry.load_catalog()

    def _resolve_model_pattern(self, pattern: str, all_models: list[tuple[str, str]]) -> list[tuple[str, str]]:
        normalized = pattern.strip()
        if not normalized:
            return []

        lower_pattern = normalized.lower()
        model_tokens = [(provider, model, f"{provider}/{model}".lower()) for provider, model in all_models]
        if any(ch in normalized for ch in "*?["):
            return [
                (provider, model)
                for provider, model, token in model_tokens
                if fnmatch(token, lower_pattern) or fnmatch(model.lower(), lower_pattern)
            ]

        for provider, model, token in model_tokens:
            if token == lower_pattern:
                return [(provider, model)]
        for provider, model, _token in model_tokens:
            if model.lower() == lower_pattern:
                return [(provider, model)]

        partial = [
            (provider, model)
            for provider, model, token in model_tokens
            if lower_pattern in token or lower_pattern in model.lower()
        ]
        if not partial:
            return []

        alias = [entry for entry in partial if self._is_model_alias(entry[1])]
        candidates = alias or partial
        candidates.sort(key=lambda item: item[1].lower(), reverse=True)
        return [candidates[0]]

    def _resolve_scoped_models(self) -> list[tuple[str, str, str | None]]:
        matched, _warnings = self._resolve_scoped_models_with_warnings()
        return matched

    def _resolve_scoped_models_with_warnings(self) -> tuple[list[tuple[str, str, str | None]], list[str]]:
        catalog = self._available_model_catalog()
        all_models = [(provider, model) for provider, models in catalog.items() for model in models]
        if not self._scoped_model_patterns:
            return ([(provider, model, None) for provider, model in all_models], [])

        warnings: list[str] = []
        default_thinking = self._settings.default_thinking_level or "off"
        matched: list[tuple[str, str, str | None]] = []
        seen: set[tuple[str, str]] = set()
        for raw_pattern in self._scoped_model_patterns:
            pattern, thinking = self.split_model_thinking(raw_pattern)
            if not pattern:
                continue
            resolved = self._resolve_model_pattern(pattern, all_models)
            if not resolved and thinking is None and ":" in raw_pattern:
                base_pattern, invalid_level = raw_pattern.rsplit(":", 1)
                fallback = self._resolve_model_pattern(base_pattern, all_models) if base_pattern else []
                if fallback:
                    warnings.append(
                        f'Invalid thinking level "{invalid_level}" in pattern "{raw_pattern}". Using default instead.'
                    )
                    resolved = fallback
            if not resolved:
                warnings.append(f'No models match pattern "{raw_pattern}"')
                continue
            effective_thinking = thinking or default_thinking
            for provider, model in resolved:
                key = (provider, model)
                if key in seen:
                    continue
                seen.add(key)
                matched.append((provider, model, effective_thinking))
        return matched, warnings

    def _prefer_models_with_auth(self, models: list[tuple[str, str, str | None]]) -> list[tuple[str, str, str | None]]:
        out: list[tuple[str, str, str | None]] = []
        for provider, model, thinking in models:
            key = self._model_registry.get_api_key_for_provider(
                provider,
                cli_api_key=self._cli_api_key,
                cli_provider=self._cli_api_key_provider,
            )
            if key:
                out.append((provider, model, thinking))
        return out or models

    def _model_supports_reasoning(self, provider: str, model_id: str) -> bool:
        definition = self._model_registry.get_model_definition(provider, model_id)
        if definition is None:
            return True
        return definition.reasoning is not False

    def _clamp_thinking_for_current_model(self) -> None:
        if not self._model_supports_reasoning(self.provider_name, self.model_id):
            self.thinking_level = "off"

    def _is_model_alias(self, model_id: str) -> bool:
        return model_id.endswith("-latest") or re.search(r"-\d{8}$", model_id) is None
