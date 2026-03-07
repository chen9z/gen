import pytest

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage, UserMessage
from gen_agent.runtime import SessionRuntime


class PlainProvider:
    async def complete(self, request):
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="ok")],
            stopReason="stop",
        )


@pytest.mark.asyncio
async def test_auto_compaction_trigger(tmp_path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    session.settings.compaction.enabled = True
    session.settings.compaction.reserve_tokens = 1
    session.settings.compaction.keep_recent_tokens = 1

    for i in range(10):
        session.session_manager.append_message(UserMessage(content=f"message {i} " + "x" * 200))

    await session.prompt("trigger")

    assert any(entry.type == "compaction" for entry in session.session_manager.entries)


@pytest.mark.asyncio
async def test_auto_compaction_keeps_recent_budget_anchor(tmp_path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    session.settings.compaction.enabled = True
    session.settings.compaction.reserve_tokens = 1
    session.settings.compaction.keep_recent_tokens = 60

    entries = []
    for i in range(4):
        entry = session.session_manager.append_message(UserMessage(content=f"message {i} " + ("x" * 180)))
        entries.append(entry)

    await session.prompt("trigger")

    compaction_entries = [entry for entry in session.session_manager.entries if entry.type == "compaction"]
    assert compaction_entries
    compaction = compaction_entries[-1]
    assert compaction.first_kept_entry_id in {entries[-1].id, entries[-2].id}


def test_compaction_context_does_not_duplicate_messages(tmp_path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    for i in range(3):
        session.session_manager.append_message(UserMessage(content=f"message {i}"))

    session._handle_manual_compact()

    context = session.session_manager.build_context().messages
    compaction_summaries = [msg for msg in context if msg.role == "compactionSummary"]
    assert len(compaction_summaries) == 2
