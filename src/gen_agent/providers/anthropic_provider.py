from __future__ import annotations

import asyncio
from typing import Any

from anthropic import Anthropic

from gen_agent.core.model_store import compute_usage_cost
from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent, Usage, UsageCost
from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.tools.base import Tool

from .base import ProviderRequest


def _to_anthropic_messages(messages: list[AgentMessage]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for msg in messages:
        role = getattr(msg, "role", "")
        if role == "user":
            content = getattr(msg, "content")
            if isinstance(content, str):
                out.append({"role": "user", "content": content})
            else:
                blocks = []
                for block in content:
                    if getattr(block, "type", "") == "text":
                        blocks.append({"type": "text", "text": block.text})
                    elif getattr(block, "type", "") == "image":
                        blocks.append(
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": block.mime_type,
                                    "data": block.data,
                                },
                            }
                        )
                out.append({"role": "user", "content": blocks})
        elif role == "assistant":
            blocks = []
            for block in getattr(msg, "content"):
                btype = getattr(block, "type", "")
                if btype == "text":
                    blocks.append({"type": "text", "text": block.text})
                elif btype == "thinking":
                    blocks.append({"type": "thinking", "thinking": block.thinking})
                elif btype == "toolCall":
                    blocks.append({"type": "tool_use", "id": block.id, "name": block.name, "input": block.arguments})
            out.append({"role": "assistant", "content": blocks or ""})
        elif role == "toolResult":
            text = "\n".join(
                block.text for block in getattr(msg, "content") if getattr(block, "type", "") == "text"
            )
            out.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": getattr(msg, "tool_call_id"),
                            "content": text,
                            "is_error": getattr(msg, "is_error"),
                        }
                    ],
                }
            )
    return out


def _tool_to_anthropic(tool: Tool) -> dict[str, Any]:
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_model.model_json_schema(),
    }


class AnthropicProvider:
    async def complete(self, request: ProviderRequest) -> AssistantMessage:
        client = Anthropic(api_key=request.api_key)

        def _call() -> Any:
            return client.messages.create(
                model=request.model_id,
                max_tokens=4096,
                system=request.system_prompt,
                messages=_to_anthropic_messages(request.messages),
                tools=[_tool_to_anthropic(tool) for tool in request.tools] or None,
            )

        resp = await asyncio.to_thread(_call)
        content_blocks: list[TextContent | ThinkingContent | ToolCallContent] = []
        stop_reason = "stop"

        for block in resp.content:
            if block.type == "text":
                content_blocks.append(TextContent(text=block.text))
            elif block.type == "thinking":
                content_blocks.append(ThinkingContent(thinking=block.thinking))
            elif block.type == "tool_use":
                content_blocks.append(ToolCallContent(id=block.id, name=block.name, arguments=dict(block.input)))
                stop_reason = "toolUse"

        usage = getattr(resp, "usage", None)
        input_tokens = getattr(usage, "input_tokens", 0) if usage else 0
        output_tokens = getattr(usage, "output_tokens", 0) if usage else 0
        cache_read_tokens = getattr(usage, "cache_read_input_tokens", 0) if usage else 0
        cache_write_tokens = getattr(usage, "cache_creation_input_tokens", 0) if usage else 0
        usage_model = Usage(
            input=input_tokens,
            output=output_tokens,
            cacheRead=cache_read_tokens,
            cacheWrite=cache_write_tokens,
            totalTokens=input_tokens + output_tokens,
            cost=UsageCost(),
        )
        usage_model.cost = compute_usage_cost("anthropic", request.model_id, usage_model)

        return AssistantMessage(
            content=content_blocks,
            api="anthropic-messages",
            provider="anthropic",
            model=request.model_id,
            usage=usage_model,
            stopReason=stop_reason,
        )
