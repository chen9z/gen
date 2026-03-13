from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.providers import ProviderRegistry, ProviderRequest
from gen_agent.providers.stream_types import ProviderStreamEvent, stream_events_from_assistant

if TYPE_CHECKING:
    from gen_agent.core.model_registry import ModelRegistry
    from gen_agent.runtime.model_controller import ModelController
    from gen_agent.tools import ToolRegistry


class ProviderRuntime:
    def __init__(
        self,
        *,
        provider_registry: ProviderRegistry,
        model_registry: "ModelRegistry",
        model_controller: "ModelController",
        tool_registry_getter: Callable[[], "ToolRegistry"],
        system_prompt_getter: Callable[[], str],
        cli_api_key: str | None,
        cli_api_key_provider: str | None,
        cli_base_url: str | None,
        cli_base_url_provider: str | None,
    ) -> None:
        self._provider_registry = provider_registry
        self._model_registry = model_registry
        self._model_controller = model_controller
        self._tool_registry_getter = tool_registry_getter
        self._system_prompt_getter = system_prompt_getter
        self._cli_api_key = cli_api_key
        self._cli_api_key_provider = cli_api_key_provider
        self._cli_base_url = cli_base_url
        self._cli_base_url_provider = cli_base_url_provider

    def build_request(self, messages: list[AgentMessage]) -> ProviderRequest | AssistantMessage:
        self._model_registry.refresh()
        provider_name = self._model_controller.provider_name
        model_id = self._model_controller.model_id
        api_key = self._model_registry.get_api_key_for_provider(
            provider_name,
            cli_api_key=self._cli_api_key,
            cli_provider=self._cli_api_key_provider,
        )
        if not api_key:
            return AssistantMessage(
                content=[
                    TextContent(
                        text=(
                            f"No API key for provider {provider_name}. "
                            "Set CLI --api-key, auth.json, environment variable, or models.json provider.apiKey."
                        )
                    )
                ],
                provider=provider_name,
                model=model_id,
                stopReason="error",
                errorMessage="missing_api_key",
            )

        runtime_model = self._model_registry.find_model(provider_name, model_id)
        resolved_base_url = runtime_model.base_url if runtime_model else None
        if self._cli_base_url and self._cli_base_url_provider == provider_name:
            resolved_base_url = self._cli_base_url
        resolved_headers = runtime_model.headers if runtime_model else None

        return ProviderRequest(
            provider=provider_name,
            model_id=model_id,
            api_key=api_key,
            system_prompt=self._system_prompt_getter(),
            messages=messages,
            tools=list(self._tool_registry_getter().tools.values()),
            thinking_level=self._model_controller.thinking_level,
            base_url=resolved_base_url,
            headers=resolved_headers,
        )

    async def complete(self, messages: list[AgentMessage]) -> AssistantMessage:
        request = self.build_request(messages)
        if isinstance(request, AssistantMessage):
            return request
        provider = self._provider_registry.get(self._transport_provider())
        return await provider.complete(request)

    async def stream(self, messages: list[AgentMessage]) -> AsyncIterator[ProviderStreamEvent]:
        request = self.build_request(messages)
        if isinstance(request, AssistantMessage):
            async for item in stream_events_from_assistant(request):
                yield item
            return

        provider = self._provider_registry.get(self._transport_provider())
        stream_method = getattr(provider, "stream_complete", None)
        if callable(stream_method):
            async for item in stream_method(request):
                yield item
            return

        fallback = await provider.complete(request)
        async for item in stream_events_from_assistant(fallback):
            yield item

    def _transport_provider(self) -> str:
        return self._model_registry.resolve_transport_provider(
            self._model_controller.provider_name,
            self._model_controller.model_id,
        )
