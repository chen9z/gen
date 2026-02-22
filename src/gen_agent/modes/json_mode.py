from __future__ import annotations

import sys
from collections.abc import Iterable

import orjson

from gen_agent.core.agent_session import AgentSession


async def run_json_mode(session: AgentSession, message: str | list[str] | None = None) -> int:
    header = session.session_manager.header
    if header:
        sys.stdout.write(orjson.dumps(header.model_dump(by_alias=True)).decode("utf-8") + "\n")

    def on_event(event):
        sys.stdout.write(orjson.dumps(event.model_dump(by_alias=True)).decode("utf-8") + "\n")
        sys.stdout.flush()

    unsub = session.subscribe(on_event)
    try:
        if isinstance(message, str) and message.strip():
            await session.prompt(message)
        elif isinstance(message, Iterable):
            prompts = [m for m in message if isinstance(m, str) and m.strip()]
            if prompts:
                for item in prompts:
                    await session.prompt(item)
            else:
                await session.continue_run()
        else:
            await session.continue_run()
    finally:
        unsub()
    last_assistant = next((m for m in reversed(session.get_messages()) if getattr(m, "role", "") == "assistant"), None)
    if last_assistant and getattr(last_assistant, "stop_reason", "") in {"error", "aborted"}:
        return 1
    return 0
