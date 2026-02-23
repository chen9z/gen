from __future__ import annotations

from types import SimpleNamespace

import pytest

from gen_agent.models.content import TextContent, ToolCallContent
from gen_agent.models.messages import AssistantMessage, ToolResultMessage, UserMessage
from gen_agent.providers.anthropic_provider import AnthropicProvider, _to_anthropic_messages
from gen_agent.providers.base import ProviderRequest
from gen_agent.providers.openai_provider import OpenAIProvider, _to_openai_messages


def test_openai_adapter_preserves_assistant_tool_calls() -> None:
    messages = [
        UserMessage(content="hello"),
        AssistantMessage(
            provider="openai",
            model="gpt-4o-mini",
            content=[
                TextContent(text="use tool"),
                ToolCallContent(id="call_1", name="read", arguments={"path": "a.txt"}),
            ],
            stopReason="toolUse",
        ),
        ToolResultMessage(
            toolCallId="call_1",
            toolName="read",
            content=[TextContent(text="file content")],
            isError=False,
        ),
    ]

    payload = _to_openai_messages(messages)
    assistant = payload[1]
    assert assistant["role"] == "assistant"
    assert assistant["tool_calls"][0]["function"]["name"] == "read"
    assert assistant["tool_calls"][0]["function"]["arguments"] == '{"path": "a.txt"}'
    tool_result = payload[2]
    assert tool_result["role"] == "tool"
    assert tool_result["tool_call_id"] == "call_1"


def test_anthropic_adapter_preserves_assistant_tool_use() -> None:
    messages = [
        UserMessage(content="hello"),
        AssistantMessage(
            provider="anthropic",
            model="claude-3-5-sonnet-latest",
            content=[
                TextContent(text="use tool"),
                ToolCallContent(id="call_1", name="read", arguments={"path": "a.txt"}),
            ],
            stopReason="toolUse",
        ),
        ToolResultMessage(
            toolCallId="call_1",
            toolName="read",
            content=[TextContent(text="file content")],
            isError=False,
        ),
    ]

    payload = _to_anthropic_messages(messages)
    assistant = payload[1]
    assert assistant["role"] == "assistant"
    assert assistant["content"][1]["type"] == "tool_use"
    assert assistant["content"][1]["name"] == "read"
    tool_result = payload[2]
    assert tool_result["role"] == "user"
    assert tool_result["content"][0]["type"] == "tool_result"
    assert tool_result["content"][0]["tool_use_id"] == "call_1"


class _AsyncChunkStream:
    def __init__(self, chunks):
        self._chunks = chunks

    def __aiter__(self):
        async def _iterate():
            for chunk in self._chunks:
                yield chunk

        return _iterate()


@pytest.mark.asyncio
async def test_openai_provider_stream_includes_system_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeCompletions:
        async def create(self, **kwargs):
            captured.update(kwargs)
            chunk_1 = SimpleNamespace(
                usage=None,
                choices=[
                    SimpleNamespace(
                        finish_reason=None,
                        delta=SimpleNamespace(content="ok", tool_calls=None),
                    )
                ],
            )
            chunk_2 = SimpleNamespace(
                usage=SimpleNamespace(
                    prompt_tokens=10,
                    completion_tokens=5,
                    total_tokens=15,
                    prompt_tokens_details=SimpleNamespace(cached_tokens=2),
                ),
                choices=[SimpleNamespace(finish_reason="stop", delta=SimpleNamespace(content=None, tool_calls=None))],
            )
            return _AsyncChunkStream([chunk_1, chunk_2])

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeOpenAI:
        def __init__(self, api_key: str, base_url: str | None = None, default_headers=None):
            captured["api_key"] = api_key
            captured["base_url"] = base_url
            captured["headers"] = default_headers
            self.chat = FakeChat()

    monkeypatch.setattr("gen_agent.providers.openai_provider.AsyncOpenAI", FakeOpenAI)

    provider = OpenAIProvider()
    request = ProviderRequest(
        provider="openai",
        model_id="gpt-4o-mini",
        api_key="test-key",
        system_prompt="System policy",
        messages=[UserMessage(content="hello")],
        tools=[],
        base_url="https://proxy.example.com/v1",
        headers={"x-test": "1"},
    )

    events = [item async for item in provider.stream_complete(request)]

    assert captured["api_key"] == "test-key"
    assert captured["base_url"] == "https://proxy.example.com/v1"
    assert captured["headers"] == {"x-test": "1"}
    assert captured["messages"][0] == {"role": "system", "content": "System policy"}
    assert any(item.type == "assistant_event" and item.event.type == "text_delta" for item in events)
    assert events[-1].type == "final"
    assert events[-1].message.content[0].text == "ok"
    assert events[-1].message.usage.input == 10
    assert events[-1].message.usage.output == 5


@pytest.mark.asyncio
async def test_openai_provider_tool_only_stream_uses_zero_based_content_index(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeCompletions:
        async def create(self, **_kwargs):
            chunk_1 = SimpleNamespace(
                usage=None,
                choices=[
                    SimpleNamespace(
                        finish_reason=None,
                        delta=SimpleNamespace(
                            content=None,
                            tool_calls=[
                                SimpleNamespace(
                                    index=0,
                                    id="call_1",
                                    function=SimpleNamespace(name="read", arguments='{"path":"a.txt"}'),
                                )
                            ],
                        ),
                    )
                ],
            )
            chunk_2 = SimpleNamespace(
                usage=SimpleNamespace(
                    prompt_tokens=10,
                    completion_tokens=5,
                    total_tokens=15,
                    prompt_tokens_details=SimpleNamespace(cached_tokens=0),
                ),
                choices=[SimpleNamespace(finish_reason="tool_calls", delta=SimpleNamespace(content=None, tool_calls=None))],
            )
            return _AsyncChunkStream([chunk_1, chunk_2])

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeOpenAI:
        def __init__(self, api_key: str, base_url: str | None = None, default_headers=None):
            _ = (api_key, base_url, default_headers)
            self.chat = FakeChat()

    monkeypatch.setattr("gen_agent.providers.openai_provider.AsyncOpenAI", FakeOpenAI)

    provider = OpenAIProvider()
    request = ProviderRequest(
        provider="openai",
        model_id="gpt-4o-mini",
        api_key="test-key",
        system_prompt="",
        messages=[UserMessage(content="hello")],
        tools=[],
    )

    events = [item async for item in provider.stream_complete(request)]
    assistant_events = [item.event for item in events if item.type == "assistant_event"]
    tool_start = next(event for event in assistant_events if event.type == "toolcall_start")
    assert tool_start.content_index == 0

    final = events[-1]
    assert final.type == "final"
    assert isinstance(final.message.content[0], ToolCallContent)
    assert final.message.content[0].name == "read"


@pytest.mark.asyncio
async def test_anthropic_provider_coerces_none_usage_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeStream:
        def __init__(self):
            self._events = [SimpleNamespace(type="text", text="ok")]

        def __aiter__(self):
            async def _iterate():
                for event in self._events:
                    yield event

            return _iterate()

        async def get_final_message(self):
            return SimpleNamespace(
                content=[SimpleNamespace(type="text", text="ok")],
                usage=SimpleNamespace(
                    input_tokens=10,
                    output_tokens=5,
                    cache_read_input_tokens=None,
                    cache_creation_input_tokens=None,
                ),
            )

    class _StreamManager:
        async def __aenter__(self):
            return FakeStream()

        async def __aexit__(self, exc_type, exc, tb):
            _ = (exc_type, exc, tb)
            return False

    class FakeMessages:
        def stream(self, **_kwargs):
            return _StreamManager()

    class FakeAnthropic:
        def __init__(self, api_key: str, base_url: str | None = None, default_headers=None):
            _ = (api_key, base_url, default_headers)
            self.messages = FakeMessages()

    monkeypatch.setattr("gen_agent.providers.anthropic_provider.AsyncAnthropic", FakeAnthropic)

    provider = AnthropicProvider()
    response = await provider.complete(
        ProviderRequest(
            provider="anthropic",
            model_id="MiniMax-M2.5",
            api_key="test-key",
            system_prompt="",
            messages=[UserMessage(content="hello")],
            tools=[],
        )
    )

    assert response.content[0].text == "ok"
    assert response.usage.input == 10
    assert response.usage.output == 5
    assert response.usage.cache_read == 0
    assert response.usage.cache_write == 0
