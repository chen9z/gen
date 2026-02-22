from __future__ import annotations

import sys
from collections.abc import Iterable

from gen_agent.core.agent_session import AgentSession


def _message_to_text(message) -> str:
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if getattr(block, "type", "") == "text":
                parts.append(block.text)
        return "\n".join(parts)
    return str(message)


async def run_print_mode(session: AgentSession, message: str | list[str] | None = None) -> int:
    prompt_list: list[str] = []
    if isinstance(message, str):
        if message.strip():
            prompt_list = [message]
    elif isinstance(message, Iterable):
        prompt_list = [m for m in message if isinstance(m, str) and m.strip()]

    if prompt_list:
        for item in prompt_list:
            await session.prompt(item)
    else:
        await session.continue_run()

    last_assistant = next((m for m in reversed(session.get_messages()) if getattr(m, "role", "") == "assistant"), None)
    if last_assistant:
        print(_message_to_text(last_assistant))
    if last_assistant and getattr(last_assistant, "stop_reason", "") in {"error", "aborted"}:
        err = getattr(last_assistant, "error_message", None) or f"Request {getattr(last_assistant, 'stop_reason', 'error')}"
        print(err, file=sys.stderr)
        return 1
    return 0
