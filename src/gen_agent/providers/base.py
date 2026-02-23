from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator, Protocol

from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.tools.base import Tool
from gen_agent.providers.stream_types import ProviderStreamEvent


@dataclass
class ProviderRequest:
    provider: str
    model_id: str
    api_key: str
    system_prompt: str
    messages: list[AgentMessage]
    tools: list[Tool]
    thinking_level: str = "off"
    base_url: str | None = None
    headers: dict[str, str] | None = None


class Provider(Protocol):
    async def complete(self, request: ProviderRequest) -> AssistantMessage:
        ...

    async def stream_complete(self, request: ProviderRequest) -> AsyncIterator[ProviderStreamEvent]:
        ...
