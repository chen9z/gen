from types import SimpleNamespace

import pytest

from gen_agent.models.content import TextContent, ToolCallContent
from gen_agent.models.messages import AssistantMessage, ToolResultMessage, UserMessage
from gen_agent.providers.base import ProviderRequest
from gen_agent.providers.anthropic_provider import _to_anthropic_messages
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


@pytest.mark.asyncio
async def test_openai_provider_includes_system_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            message = SimpleNamespace(content="ok", tool_calls=[])
            return SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=None)

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeOpenAI:
        def __init__(
            self,
            api_key: str,
            base_url: str | None = None,
            default_headers: dict[str, str] | None = None,
        ):
            captured["api_key"] = api_key
            captured["base_url"] = base_url
            captured["headers"] = default_headers
            self.chat = FakeChat()

    monkeypatch.setattr("gen_agent.providers.openai_provider.OpenAI", FakeOpenAI)

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

    await provider.complete(request)

    assert captured["api_key"] == "test-key"
    assert captured["base_url"] == "https://proxy.example.com/v1"
    assert captured["headers"] == {"x-test": "1"}
    assert captured["messages"][0] == {"role": "system", "content": "System policy"}
