from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from anthropic import AsyncAnthropic

from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent
from gen_agent.models.events import AssistantMessageEvent
from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.tools.base import Tool

from .base import ProviderRequest
from .stream_types import (
    build_usage,
    coerce_usage_int,
    complete_from_stream,
    ProviderAssistantEvent,
    ProviderFinalEvent,
    ProviderStreamEvent,
    StreamUsage,
)


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
            continue

        if role == "assistant":
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
            continue

        if role == "toolResult":
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
    async def stream_complete(self, request: ProviderRequest) -> AsyncIterator[ProviderStreamEvent]:
        client = AsyncAnthropic(
            api_key=request.api_key,
            base_url=request.base_url,
            default_headers=request.headers,
        )

        text_started = False
        thinking_started = False
        tool_started: set[int] = set()
        text_value = ""
        thinking_value = ""

        async with client.messages.stream(
            model=request.model_id,
            max_tokens=4096,
            system=request.system_prompt,
            messages=_to_anthropic_messages(request.messages),
            tools=[_tool_to_anthropic(tool) for tool in request.tools] or None,
        ) as stream:
            async for event in stream:
                etype = getattr(event, "type", "")
                if etype == "text":
                    if not text_started:
                        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
                        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_start", contentIndex=0))
                        text_started = True
                    delta = getattr(event, "text", "") or ""
                    if delta:
                        text_value += delta
                        yield ProviderAssistantEvent(
                            event=AssistantMessageEvent(type="text_delta", contentIndex=0, delta=delta)
                        )
                    continue

                if etype == "thinking":
                    if not thinking_started:
                        if not text_started:
                            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
                            text_started = True
                        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="thinking_start", contentIndex=1))
                        thinking_started = True
                    delta = getattr(event, "thinking", "") or ""
                    if delta:
                        thinking_value += delta
                        yield ProviderAssistantEvent(
                            event=AssistantMessageEvent(type="thinking_delta", contentIndex=1, delta=delta)
                        )
                    continue

                if etype == "content_block_start":
                    block = getattr(event, "content_block", None)
                    if getattr(block, "type", "") != "tool_use":
                        continue
                    idx = int(getattr(event, "index", 0) or 0)
                    if idx in tool_started:
                        continue
                    tool_started.add(idx)
                    if not text_started:
                        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
                        text_started = True
                    yield ProviderAssistantEvent(event=AssistantMessageEvent(type="toolcall_start", contentIndex=idx))
                    name = getattr(block, "name", None)
                    if name:
                        yield ProviderAssistantEvent(
                            event=AssistantMessageEvent(type="toolcall_delta", contentIndex=idx, delta=str(name))
                        )
                    continue

                if etype == "input_json":
                    idx = int(getattr(event, "index", 0) or 0)
                    partial = getattr(event, "partial_json", "") or ""
                    if partial:
                        yield ProviderAssistantEvent(
                            event=AssistantMessageEvent(type="toolcall_delta", contentIndex=idx, delta=partial)
                        )
                    continue

                if etype == "content_block_stop":
                    block = getattr(event, "content_block", None)
                    if getattr(block, "type", "") != "tool_use":
                        continue
                    idx = int(getattr(event, "index", 0) or 0)
                    yield ProviderAssistantEvent(event=AssistantMessageEvent(type="toolcall_end", contentIndex=idx))

            final = await stream.get_final_message()

        usage_raw = getattr(final, "usage", None)
        input_tokens = coerce_usage_int(getattr(usage_raw, "input_tokens", 0) if usage_raw else 0)
        output_tokens = coerce_usage_int(getattr(usage_raw, "output_tokens", 0) if usage_raw else 0)
        cache_read_tokens = coerce_usage_int(getattr(usage_raw, "cache_read_input_tokens", 0) if usage_raw else 0)
        cache_write_tokens = coerce_usage_int(getattr(usage_raw, "cache_creation_input_tokens", 0) if usage_raw else 0)
        usage = StreamUsage(
            input=input_tokens,
            output=output_tokens,
            cache_read=cache_read_tokens,
            cache_write=cache_write_tokens,
            total_tokens=input_tokens + output_tokens,
        )

        content_blocks: list[TextContent | ThinkingContent | ToolCallContent] = []
        stop_reason = "stop"
        for block in final.content:
            if block.type == "text":
                content_blocks.append(TextContent(text=block.text))
            elif block.type == "thinking":
                content_blocks.append(ThinkingContent(thinking=block.thinking))
            elif block.type == "tool_use":
                content_blocks.append(ToolCallContent(id=block.id, name=block.name, arguments=dict(block.input)))
                stop_reason = "toolUse"

        if text_started:
            if text_value:
                yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_end", contentIndex=0))
            if thinking_started:
                yield ProviderAssistantEvent(event=AssistantMessageEvent(type="thinking_end", contentIndex=1))
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="done"))
        else:
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="done"))

        message = AssistantMessage(
            content=content_blocks,
            api="anthropic-messages",
            provider=request.provider,
            model=request.model_id,
            usage=build_usage(request.provider, request.model_id, usage),
            stopReason=stop_reason,
        )
        yield ProviderFinalEvent(message=message)

    async def complete(self, request: ProviderRequest) -> AssistantMessage:
        return await complete_from_stream(self.stream_complete(request), "Anthropic")
