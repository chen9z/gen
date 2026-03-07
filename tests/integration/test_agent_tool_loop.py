import pytest

from gen_agent.core.agent_loop import run_agent_loop
from gen_agent.models.content import TextContent, ToolCallContent
from gen_agent.models.messages import AssistantMessage
from gen_agent.runtime import SessionRuntime


class FakeProvider:
    def __init__(self):
        self.calls = 0

    async def complete(self, request):
        self.calls += 1
        has_tool_result = any(getattr(m, "role", "") == "toolResult" for m in request.messages)
        if not has_tool_result:
            return AssistantMessage(
                provider=request.provider,
                model=request.model_id,
                content=[ToolCallContent(id="call_1", name="ls", arguments={"path": "."})],
                stopReason="toolUse",
            )
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="Done")],
            stopReason="stop",
        )


@pytest.mark.asyncio
async def test_agent_runs_tool_loop(tmp_path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    fake = FakeProvider()
    session.provider_registry._providers["openai"] = fake

    new_messages = await session.prompt("list files")

    roles = [getattr(m, "role", "") for m in new_messages]
    assert roles.count("assistant") >= 2
    assert "toolResult" in roles
    assert fake.calls >= 2


class ContinueProvider:
    async def complete(self, request):
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="continued")],
            stopReason="stop",
        )


@pytest.mark.asyncio
async def test_continue_run_persists_generated_messages(tmp_path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = ContinueProvider()

    new_messages = await session.continue_run()
    assert len(new_messages) == 1
    assert new_messages[0].role == "assistant"

    persisted = session.get_messages()
    assert len(persisted) == 1
    assert persisted[0].role == "assistant"
    assert persisted[0].content[0].text == "continued"


class EndlessToolProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def complete(self, _messages):
        self.calls += 1
        return AssistantMessage(
            provider="openai",
            model="gpt-4o-mini",
            content=[ToolCallContent(id=f"call_{self.calls}", name="ls", arguments={"path": "."})],
            stopReason="toolUse",
        )


@pytest.mark.asyncio
async def test_agent_loop_enforces_max_turns_for_repeated_tool_calls():
    provider = EndlessToolProvider()

    async def exec_tool(_name, _args):
        return [TextContent(text="ok")], None, False

    messages = await run_agent_loop(
        prompts=[],
        context_messages=[],
        provider_call=provider.complete,
        exec_tool=exec_tool,
        emit=lambda _event: None,
        max_turns=2,
    )

    assert provider.calls == 2
    roles = [getattr(m, "role", "") for m in messages]
    assert roles.count("assistant") == 2
    assert roles.count("toolResult") == 2
