from __future__ import annotations

import pytest

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.content import TextContent, ToolCallContent
from gen_agent.models.events import AssistantMessageEvent
from gen_agent.models.messages import AssistantMessage
from gen_agent.providers.stream_types import ProviderAssistantEvent, ProviderFinalEvent, stream_events_from_assistant


class StreamingProvider:
    def __init__(self) -> None:
        self.complete_calls = 0
        self.stream_calls = 0

    async def complete(self, request):
        _ = request
        self.complete_calls += 1
        raise AssertionError("complete() should not be called when stream_complete exists")

    async def stream_complete(self, request):
        _ = request
        self.stream_calls += 1
        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="start"))
        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_start", contentIndex=0))
        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_delta", contentIndex=0, delta="hi"))
        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="text_end", contentIndex=0))
        yield ProviderAssistantEvent(event=AssistantMessageEvent(type="done"))
        yield ProviderFinalEvent(
            message=AssistantMessage(
                provider=request.provider,
                model=request.model_id,
                content=[TextContent(text="hi")],
                stopReason="stop",
            )
        )


@pytest.mark.asyncio
async def test_agent_session_prefers_provider_stream_complete(tmp_path) -> None:
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    provider = StreamingProvider()
    session.provider_registry._providers["openai"] = provider

    events: list[str] = []

    def _listener(event):
        if event.type == "message_update":
            events.append(event.assistant_message_event.type)

    session.subscribe(_listener)
    await session.prompt("hello")

    assert provider.stream_calls == 1
    assert provider.complete_calls == 0
    assert "text_delta" in events
    assert events[-1] == "done"


@pytest.mark.asyncio
async def test_stream_events_from_assistant_serializes_tool_args_as_json() -> None:
    message = AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[ToolCallContent(id="call_1", name="read", arguments={"path": "a.txt"})],
        stopReason="toolUse",
    )

    events = [item async for item in stream_events_from_assistant(message)]
    deltas = [
        item.event.delta
        for item in events
        if item.type == "assistant_event" and item.event.type == "toolcall_delta"
    ]

    assert '{"path": "a.txt"}' in deltas
    assert "{'path': 'a.txt'}" not in deltas
