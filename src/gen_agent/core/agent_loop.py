from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

from gen_agent.models.content import TextContent, ThinkingContent, ToolCallContent, UserContentBlock
from gen_agent.models.events import (
    AssistantMessageEvent,
    AgentEnd,
    AgentEvent,
    AgentStart,
    MessageEnd,
    MessageStart,
    MessageUpdate,
    ToolExecutionEnd,
    ToolExecutionStart,
    TurnEnd,
    TurnStart,
)
from gen_agent.models.messages import AgentMessage, AssistantMessage, ToolResultMessage

EmitFn = Callable[[AgentEvent], None]
ToolExec = Callable[[str, dict[str, Any]], Awaitable[tuple[list[UserContentBlock], Any, bool]]]
ProviderCall = Callable[[list[AgentMessage]], Awaitable[AssistantMessage]]
QueuedFn = Callable[[], list[AgentMessage]]


def _assistant_events(assistant: AssistantMessage) -> list[AssistantMessageEvent]:
    events: list[AssistantMessageEvent] = [AssistantMessageEvent(type="start")]
    for idx, block in enumerate(assistant.content):
        if isinstance(block, TextContent):
            events.append(AssistantMessageEvent(type="text_start", contentIndex=idx))
            if block.text:
                events.append(AssistantMessageEvent(type="text_delta", contentIndex=idx, delta=block.text))
            events.append(AssistantMessageEvent(type="text_end", contentIndex=idx))
        elif isinstance(block, ThinkingContent):
            events.append(AssistantMessageEvent(type="thinking_start", contentIndex=idx))
            if block.thinking:
                events.append(AssistantMessageEvent(type="thinking_delta", contentIndex=idx, delta=block.thinking))
            events.append(AssistantMessageEvent(type="thinking_end", contentIndex=idx))
        elif isinstance(block, ToolCallContent):
            events.append(AssistantMessageEvent(type="toolcall_start", contentIndex=idx))
            if block.name:
                events.append(AssistantMessageEvent(type="toolcall_delta", contentIndex=idx, delta=block.name))
            args_json = json.dumps(block.arguments, ensure_ascii=False)
            if args_json and args_json != "{}":
                events.append(AssistantMessageEvent(type="toolcall_delta", contentIndex=idx, delta=args_json))
            events.append(AssistantMessageEvent(type="toolcall_end", contentIndex=idx))

    if assistant.stop_reason == "error":
        events.append(AssistantMessageEvent(type="error", error=assistant.error_message or "provider_error"))
    events.append(AssistantMessageEvent(type="done"))
    return events


async def run_agent_loop(
    prompts: list[AgentMessage],
    context_messages: list[AgentMessage],
    provider_call: ProviderCall,
    exec_tool: ToolExec,
    emit: EmitFn,
    get_steering_messages: QueuedFn | None = None,
    get_follow_up_messages: QueuedFn | None = None,
    max_turns: int = 30,
) -> list[AgentMessage]:
    new_messages: list[AgentMessage] = []
    messages = list(context_messages)

    emit(AgentStart())
    emit(TurnStart())

    for prompt in prompts:
        messages.append(prompt)
        new_messages.append(prompt)
        emit(MessageStart(message=prompt))
        emit(MessageEnd(message=prompt))

    first_turn = True
    pending_messages: list[AgentMessage] = get_steering_messages() if get_steering_messages else []

    turns_used = 0
    while turns_used < max_turns:
        has_more_tool_calls = True
        while (has_more_tool_calls or pending_messages) and turns_used < max_turns:
            if not first_turn:
                emit(TurnStart())
            first_turn = False
            turns_used += 1

            if pending_messages:
                for pending in pending_messages:
                    messages.append(pending)
                    new_messages.append(pending)
                    emit(MessageStart(message=pending))
                    emit(MessageEnd(message=pending))
                pending_messages = []

            assistant = await provider_call(messages)
            messages.append(assistant)
            new_messages.append(assistant)
            emit(MessageStart(message=assistant))
            for assistant_event in _assistant_events(assistant):
                emit(MessageUpdate(message=assistant, assistantMessageEvent=assistant_event))
            emit(MessageEnd(message=assistant))

            if assistant.stop_reason in ("error", "aborted"):
                emit(TurnEnd(message=assistant, toolResults=[]))
                emit(AgentEnd(messages=new_messages))
                return new_messages

            tool_calls = [block for block in assistant.content if isinstance(block, ToolCallContent)]
            has_more_tool_calls = bool(tool_calls)
            tool_results: list[ToolResultMessage] = []

            for call in tool_calls:
                emit(ToolExecutionStart(toolCallId=call.id, toolName=call.name, args=call.arguments))
                try:
                    text_blocks, details, is_error = await exec_tool(call.name, call.arguments)
                    result = ToolResultMessage(
                        toolCallId=call.id,
                        toolName=call.name,
                        content=text_blocks,
                        details=details,
                        isError=is_error,
                    )
                except Exception as exc:
                    result = ToolResultMessage(
                        toolCallId=call.id,
                        toolName=call.name,
                        content=[TextContent(text=str(exc))],
                        isError=True,
                    )
                    is_error = True

                messages.append(result)
                new_messages.append(result)
                tool_results.append(result)
                emit(MessageStart(message=result))
                emit(MessageEnd(message=result))
                emit(
                    ToolExecutionEnd(
                        toolCallId=call.id,
                        toolName=call.name,
                        result=result.model_dump(by_alias=True),
                        isError=is_error,
                    )
                )

            emit(TurnEnd(message=assistant, toolResults=tool_results))
            pending_messages = get_steering_messages() if get_steering_messages else []

        if turns_used >= max_turns:
            break

        follow = get_follow_up_messages() if get_follow_up_messages else []
        if follow:
            pending_messages = follow
            continue

        break

    emit(AgentEnd(messages=new_messages))
    return new_messages
