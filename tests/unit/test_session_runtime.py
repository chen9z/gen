from __future__ import annotations

import pytest

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage
from gen_agent.runtime import SessionRuntime


class _PlainProvider:
    async def complete(self, request):
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="ok")],
            stopReason="stop",
        )


class _RetryProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def complete(self, request):
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("retry-me")
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="retry-ok")],
            stopReason="stop",
        )


@pytest.mark.asyncio
async def test_session_runtime_emits_event_envelope(tmp_path) -> None:
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = _PlainProvider()

    events = []
    session.subscribe(events.append)

    await session.prompt("hello")

    assert events
    run_ids = {event.run_id for event in events if event.run_id}
    assert len(run_ids) == 1
    assert {event.actor_id for event in events} == {"main"}
    assert {event.parent_run_id for event in events} == {None}
    assert {event.session_id for event in events} == {session.session_manager.header.id}


@pytest.mark.asyncio
async def test_session_runtime_reuses_run_id_during_retry(tmp_path) -> None:
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.settings.retry.enabled = True
    session.settings.retry.max_retries = 1
    provider = _RetryProvider()
    session.provider_registry._providers["openai"] = provider

    captured: list[tuple[str, str | None]] = []

    def _listener(event) -> None:
        if event.type in {"auto_retry_start", "agent_end"}:
            captured.append((event.type, event.run_id))

    session.subscribe(_listener)
    await session.prompt("hello")

    assert provider.calls == 2
    assert captured[0][0] == "auto_retry_start"
    assert captured[1][0] == "agent_end"
    assert captured[0][1]
    assert captured[0][1] == captured[1][1]
