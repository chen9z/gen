from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI

from gen_agent.models.content import TextContent, ToolCallContent
from gen_agent.models.events import AssistantMessageEvent
from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.tools.base import Tool

from .base import ProviderRequest
from .stream_types import (
    ProviderAssistantEvent,
    ProviderFinalEvent,
    ProviderStreamEvent,
    StreamUsage,
    build_usage,
)


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
            continue

        if role == "assistant":
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

            payload: dict[str, Any] = {"role": "assistant", "content": text or None}
            if tool_calls:
                payload["tool_calls"] = tool_calls
            out.append(payload)
            continue

        if role == "toolResult":
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


def _stop_reason_from_finish(finish_reason: str | None, has_tool_calls: bool) -> str:
    if finish_reason in {"tool_calls", "function_call"} or has_tool_calls:
        return "toolUse"
    if finish_reason == "length":
        return "length"
    return "stop"


class OpenAIProvider:
    async def stream_complete(self, request: ProviderRequest) -> AsyncIterator[ProviderStreamEvent]:
        client = AsyncOpenAI(
            api_key=request.api_key,
            base_url=request.base_url,
            default_headers=request.headers,
        )

        messages = _to_openai_messages(request.messages)
        if request.system_prompt:
            messages = [{"role": "system", "content": request.system_prompt}, *messages]

        stream = await client.chat.completions.create(
            model=request.model_id,
            messages=messages,
            tools=[_tool_to_openai(tool) for tool in request.tools] or None,
            stream=True,
            stream_options={"include_usage": True},
        )

        text_value = ""
        text_started = False
        text_index: int | None = None

        tool_index_map: dict[int, int] = {}
        tool_ids: dict[int, str] = {}
        tool_names: dict[int, str] = {}
        tool_args: dict[int, str] = {}
        tool_started: set[int] = set()
        next_content_index = 0

        usage = StreamUsage()
        finish_reason: str | None = None

        async for chunk in stream:
            usage_raw = getattr(chunk, "usage", None)
            if usage_raw is not None:
                prompt_details = getattr(usage_raw, "prompt_tokens_details", None)
                usage = StreamUsage(
                    input=int(getattr(usage_raw, "prompt_tokens", 0) or 0),
                    output=int(getattr(usage_raw, "completion_tokens", 0) or 0),
                    cache_read=int(getattr(prompt_details, "cached_tokens", 0) or 0) if prompt_details else 0,
                    cache_write=0,
                    total_tokens=int(getattr(usage_raw, "total_tokens", 0) or 0),
                )

            if not getattr(chunk, "choices", None):
                continue
            choice = chunk.choices[0]
            if getattr(choice, "finish_reason", None):
                finish_reason = choice.finish_reason

            delta = getattr(choice, "delta", None)
            if delta is None:
                continue

            text_delta = getattr(delta, "content", None)
            if text_delta:
                if text_index is None:
                    if not text_started:
                        text_started = True
                        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
                    text_started = True
                    text_index = next_content_index
                    next_content_index += 1
                    yield ProviderAssistantEvent(
                        event=AssistantMessageEvent(type="text_start", contentIndex=text_index)
                    )
                assert text_index is not None
                text_value += text_delta
                yield ProviderAssistantEvent(
                    event=AssistantMessageEvent(type="text_delta", contentIndex=text_index, delta=text_delta)
                )

            for call in getattr(delta, "tool_calls", None) or []:
                raw_index = getattr(call, "index", 0) or 0
                if raw_index not in tool_index_map:
                    tool_index_map[raw_index] = next_content_index
                    next_content_index += 1
                content_index = tool_index_map[raw_index]
                if raw_index not in tool_started:
                    if not text_started:
                        text_started = True
                        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
                    yield ProviderAssistantEvent(
                        event=AssistantMessageEvent(type="toolcall_start", contentIndex=content_index)
                    )
                    tool_started.add(raw_index)

                call_id = getattr(call, "id", None)
                if call_id:
                    tool_ids[raw_index] = call_id

                function = getattr(call, "function", None)
                if function is None:
                    continue
                name_delta = getattr(function, "name", None)
                if name_delta:
                    tool_names[raw_index] = (tool_names.get(raw_index) or "") + name_delta
                    yield ProviderAssistantEvent(
                        event=AssistantMessageEvent(type="toolcall_delta", contentIndex=content_index, delta=name_delta)
                    )
                args_delta = getattr(function, "arguments", None)
                if args_delta:
                    tool_args[raw_index] = tool_args.get(raw_index, "") + args_delta
                    yield ProviderAssistantEvent(
                        event=AssistantMessageEvent(type="toolcall_delta", contentIndex=content_index, delta=args_delta)
                    )

        if text_started and text_value and text_index is not None:
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_end", contentIndex=text_index))

        content_by_index: dict[int, TextContent | ToolCallContent] = {}
        if text_index is not None and text_value:
            content_by_index[text_index] = TextContent(text=text_value)

        tool_calls: list[ToolCallContent] = []
        for raw_index in sorted(tool_index_map.keys()):
            content_index = tool_index_map[raw_index]
            raw_args = tool_args.get(raw_index, "")
            try:
                parsed = json.loads(raw_args) if raw_args else {}
            except Exception:
                parsed = {}
            call = ToolCallContent(
                id=tool_ids.get(raw_index) or f"call_{raw_index}",
                name=tool_names.get(raw_index) or "tool",
                arguments=parsed,
            )
            tool_calls.append(call)
            content_by_index[content_index] = call
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="toolcall_end", contentIndex=content_index))

        if text_started:
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="done"))

        stop_reason = _stop_reason_from_finish(finish_reason, has_tool_calls=bool(tool_calls))
        ordered_content = [content_by_index[idx] for idx in sorted(content_by_index)]
        message = AssistantMessage(
            content=ordered_content,
            api="openai-chat-completions",
            provider=request.provider,
            model=request.model_id,
            usage=build_usage(request.provider, request.model_id, usage),
            stopReason=stop_reason,
        )
        if not text_started:
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
            yield ProviderAssistantEvent(event=AssistantMessageEvent(type="done"))
        yield ProviderFinalEvent(message=message)

    async def complete(self, request: ProviderRequest) -> AssistantMessage:
        final_message: AssistantMessage | None = None
        async for item in self.stream_complete(request):
            if item.type == "final":
                final_message = item.message
        if final_message is None:
            raise RuntimeError("OpenAI stream ended without final message")
        return final_message
