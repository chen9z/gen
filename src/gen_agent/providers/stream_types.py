from __future__ import annotations

import json
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any, Literal

from gen_agent.core.model_store import compute_usage_cost
from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent, Usage, UsageCost
from gen_agent.models.events import AssistantMessageEvent
from gen_agent.models.messages import AssistantMessage


@dataclass
class StreamUsage:
    input: int = 0
    output: int = 0
    cache_read: int = 0
    cache_write: int = 0
    total_tokens: int = 0


@dataclass
class ProviderAssistantEvent:
    type: Literal["assistant_event"] = "assistant_event"
    event: AssistantMessageEvent = field(default_factory=lambda: AssistantMessageEvent(type="start"))


@dataclass
class ProviderFinalEvent:
    type: Literal["final"] = "final"
    message: AssistantMessage = field(default_factory=lambda: AssistantMessage(content=[]))


ProviderStreamEvent = ProviderAssistantEvent | ProviderFinalEvent


def build_usage(provider: str, model_id: str, usage: StreamUsage | None) -> Usage:
    if usage is None:
        usage_model = Usage()
    else:
        usage_model = Usage(
            input=max(0, usage.input),
            output=max(0, usage.output),
            cacheRead=max(0, usage.cache_read),
            cacheWrite=max(0, usage.cache_write),
            totalTokens=max(0, usage.total_tokens),
            cost=UsageCost(),
        )
    usage_model.cost = compute_usage_cost(provider, model_id, usage_model)
    return usage_model


def build_assistant_from_stream(
    provider: str,
    model_id: str,
    text: str,
    thinking: str | None,
    tool_calls: list[ToolCallContent],
    stop_reason: Literal["stop", "length", "toolUse", "error", "aborted"] = "stop",
    error_message: str | None = None,
    usage: StreamUsage | None = None,
    api: str = "chat",
) -> AssistantMessage:
    content: list[TextContent | ThinkingContent | ToolCallContent] = []
    if text:
        content.append(TextContent(text=text))
    if thinking:
        content.append(ThinkingContent(thinking=thinking))
    content.extend(tool_calls)
    if tool_calls and stop_reason == "stop":
        stop_reason = "toolUse"
    return AssistantMessage(
        content=content,
        api=api,
        provider=provider,
        model=model_id,
        usage=build_usage(provider, model_id, usage),
        stopReason=stop_reason,
        errorMessage=error_message,
    )


async def stream_events_from_assistant(message: AssistantMessage) -> AsyncIterator[ProviderStreamEvent]:
    yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
    for idx, block in enumerate(message.content):
        if isinstance(block, TextContent):
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_start", contentIndex=idx))
            if block.text:
                yield ProviderAssistantEvent(
                    event=AssistantMessageEvent(type="text_delta", contentIndex=idx, delta=block.text)
                )
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_end", contentIndex=idx))
            continue
        if isinstance(block, ThinkingContent):
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="thinking_start", contentIndex=idx))
            if block.thinking:
                yield ProviderAssistantEvent(
                    event=AssistantMessageEvent(type="thinking_delta", contentIndex=idx, delta=block.thinking)
                )
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="thinking_end", contentIndex=idx))
            continue
        if isinstance(block, ToolCallContent):
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="toolcall_start", contentIndex=idx))
            if block.name:
                yield ProviderAssistantEvent(
                    event=AssistantMessageEvent(type="toolcall_delta", contentIndex=idx, delta=block.name)
                )
            args_json = json.dumps(block.arguments, ensure_ascii=False)
            if args_json and args_json != "{}":
                yield ProviderAssistantEvent(
                    event=AssistantMessageEvent(type="toolcall_delta", contentIndex=idx, delta=args_json)
                )
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="toolcall_end", contentIndex=idx))

    if message.stop_reason == "error":
        yield ProviderAssistantEvent(
            event=AssistantMessageEvent(type="error", error=message.error_message or "provider_error")
        )
    yield ProviderAssistantEvent(event=AssistantMessageEvent(type="done"))
    yield ProviderFinalEvent(message=message)


def coerce_usage_int(value: Any) -> int:
    """Safely coerce a usage token count (may be None) to int."""
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


async def complete_from_stream(
    stream_fn: Any,
    provider_label: str,
) -> AssistantMessage:
    """Consume a stream_complete() iterator and return the final message."""
    final_message: AssistantMessage | None = None
    async for item in stream_fn:
        if item.type == "final":
            final_message = item.message
    if final_message is None:
        raise RuntimeError(f"{provider_label} stream ended without final message")
    return final_message
