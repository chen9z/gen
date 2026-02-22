from __future__ import annotations

import os
from pathlib import Path

from gen_agent.models.settings import ApiKeyCredential, AuthCredential, AuthModel

from .paths import auth_path, ensure_dir


class AuthStore:
    def __init__(self, path: Path | None = None):
        self.path = path or auth_path()
        self._model = self._load()

    def _load(self) -> AuthModel:
        if not self.path.exists():
            return AuthModel()
        try:
            import json

            data = json.loads(self.path.read_text(encoding="utf-8"))
            if "providers" not in data:
                data = {"providers": data}
            return AuthModel.model_validate(data)
        except Exception:
            return AuthModel()

    def _save(self) -> None:
        ensure_dir(self.path.parent)
        self.path.write_text(self._model.model_dump_json(indent=2, by_alias=True, exclude_none=True), encoding="utf-8")

    def set(self, provider: str, cred: AuthCredential) -> None:
        self._model.providers[provider] = cred
        self._save()

    def remove(self, provider: str) -> None:
        self._model.providers.pop(provider, None)
        self._save()

    def get(self, provider: str) -> AuthCredential | None:
        return self._model.providers.get(provider)

    def get_api_key(
        self,
        provider: str,
        cli_api_key: str | None = None,
        cli_provider: str | None = None,
    ) -> str | None:
        if cli_api_key and (cli_provider is None or cli_provider == provider):
            return cli_api_key

        env_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
        }
        env_key = env_map.get(provider)
        if env_key and os.environ.get(env_key):
            return os.environ[env_key]

        cred = self.get(provider)
        if isinstance(cred, ApiKeyCredential) or (cred and getattr(cred, "type", None) == "api_key"):
            return getattr(cred, "key", None)

        return None
