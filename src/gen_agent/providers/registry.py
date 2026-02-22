from __future__ import annotations

from gen_agent.providers.base import Provider

from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, Provider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
        }

    def get(self, provider: str) -> Provider:
        if provider not in self._providers:
            raise ValueError(f"Unsupported provider: {provider}")
        return self._providers[provider]

    def list_names(self) -> list[str]:
        return sorted(self._providers.keys())
