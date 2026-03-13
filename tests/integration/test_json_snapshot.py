import json
from pathlib import Path

import pytest

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage
from gen_agent.modes.json_mode import run_json_mode
from gen_agent.runtime import SessionRuntime


class PlainProvider:
    async def complete(self, request):
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="snapshot")],
            stopReason="stop",
        )


@pytest.mark.asyncio
async def test_json_mode_nonzero_on_provider_error(tmp_path: Path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key=None,
        persist_session=False,
    )

    code = await run_json_mode(session, "hello")
    assert code == 1


@pytest.mark.asyncio
async def test_json_event_types_snapshot(tmp_path: Path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    event_types = []

    def on_event(event):
        event_types.append(event.type)

    unsub = session.subscribe(on_event)
    try:
        await session.prompt("hello")
    finally:
        unsub()

    golden = Path(__file__).resolve().parents[1] / "golden" / "json_event_stream.golden"
    expected_types = []
    for line in golden.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected_types.append(json.loads(line)["type"])

    expected_without_session = [t for t in expected_types if t != "session"]
    assert event_types[:4] == expected_without_session[:4]
    assert event_types[-1] == "agent_end"


@pytest.mark.asyncio
async def test_assistant_message_update_events_include_text_flow(tmp_path: Path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    assistant_event_types: list[str] = []

    def on_event(event):
        if event.type == "message_update":
            assistant_event_types.append(event.assistant_message_event.type)

    unsub = session.subscribe(on_event)
    try:
        await session.prompt("hello")
    finally:
        unsub()

    assert assistant_event_types[:4] == ["start", "text_start", "text_delta", "text_end"]
    assert assistant_event_types[-1] == "done"
