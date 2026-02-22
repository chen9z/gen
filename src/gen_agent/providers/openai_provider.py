from __future__ import annotations

import asyncio
import json
from typing import Any

from openai import OpenAI

from gen_agent.core.model_store import compute_usage_cost
from gen_agent.models.content import TextContent, ToolCallContent, Usage, UsageCost
from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.tools.base import Tool

from .base import ProviderRequest


def _to_openai_messages(messages: list[AgentMessage]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for msg in messages:
        role = getattr(msg, "role", "")
        if role == "user":
            content = getattr(msg, "content")
            if isinstance(content, str):
                out.append({"role": "user", "content": content})
            else:
                parts = []
                for block in content:
                    if getattr(block, "type", "") == "text":
                        parts.append({"type": "text", "text": block.text})
                    elif getattr(block, "type", "") == "image":
                        parts.append(
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{block.mime_type};base64,{block.data}"},
                            }
                        )
                out.append({"role": "user", "content": parts})
        elif role == "assistant":
            content_blocks = getattr(msg, "content")
            text = "\n".join(block.text for block in content_blocks if getattr(block, "type", "") == "text")
            tool_calls = []
            for block in content_blocks:
                if getattr(block, "type", "") != "toolCall":
                    continue
                tool_calls.append(
                    {
                        "id": block.id,
                        "type": "function",
                        "function": {
                            "name": block.name,
                            "arguments": json.dumps(block.arguments, ensure_ascii=False),
                        },
                    }
                )

            payload: dict[str, Any] = {"role": "assistant"}
            if text:
                payload["content"] = text
            else:
                payload["content"] = None
            if tool_calls:
                payload["tool_calls"] = tool_calls
            out.append(payload)
        elif role == "toolResult":
            text = "\n".join(
                block.text for block in getattr(msg, "content") if getattr(block, "type", "") == "text"
            )
            out.append(
                {
                    "role": "tool",
                    "tool_call_id": getattr(msg, "tool_call_id"),
                    "name": getattr(msg, "tool_name"),
                    "content": text,
                }
            )
    return out


def _tool_to_openai(tool: Tool) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_model.model_json_schema(),
        },
    }


class OpenAIProvider:
    async def complete(self, request: ProviderRequest) -> AssistantMessage:
        client = OpenAI(
            api_key=request.api_key,
            base_url=request.base_url,
            default_headers=request.headers,
        )

        def _call() -> Any:
            messages = _to_openai_messages(request.messages)
            if request.system_prompt:
                messages = [{"role": "system", "content": request.system_prompt}, *messages]
            return client.chat.completions.create(
                model=request.model_id,
                messages=messages,
                tools=[_tool_to_openai(tool) for tool in request.tools] or None,
            )

        resp = await asyncio.to_thread(_call)
        choice = resp.choices[0]
        content_blocks: list[TextContent | ToolCallContent] = []

        if getattr(choice.message, "content", None):
            content_blocks.append(TextContent(text=choice.message.content))

        for call in choice.message.tool_calls or []:
            try:
                args = json.loads(call.function.arguments or "{}")
            except Exception:
                args = {}
            content_blocks.append(
                ToolCallContent(
                    id=call.id,
                    name=call.function.name,
                    arguments=args,
                )
            )

        stop_reason = "toolUse" if choice.message.tool_calls else "stop"
        usage = getattr(resp, "usage", None)
        prompt_details = getattr(usage, "prompt_tokens_details", None) if usage else None

        usage_model = Usage(
            input=getattr(usage, "prompt_tokens", 0) if usage else 0,
            output=getattr(usage, "completion_tokens", 0) if usage else 0,
            cacheRead=getattr(prompt_details, "cached_tokens", 0) if prompt_details else 0,
            totalTokens=getattr(usage, "total_tokens", 0) if usage else 0,
            cost=UsageCost(),
        )
        usage_model.cost = compute_usage_cost(request.provider, request.model_id, usage_model)

        return AssistantMessage(
            content=content_blocks,
            api="openai-chat-completions",
            provider=request.provider,
            model=request.model_id,
            usage=usage_model,
            stopReason=stop_reason,
        )
