from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.tools.base import Tool


@dataclass
class ProviderRequest:
    provider: str
    model_id: str
    api_key: str
    system_prompt: str
    messages: list[AgentMessage]
    tools: list[Tool]
    thinking_level: str = "off"


class Provider(Protocol):
    async def complete(self, request: ProviderRequest) -> AssistantMessage:
        ...
