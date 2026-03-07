from __future__ import annotations

import sys
from collections.abc import Iterable

from gen_agent.models.prompt import PromptInput
from gen_agent.runtime import SessionRuntime


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


def _normalize_prompts(message: str | PromptInput | Iterable[str | PromptInput] | None) -> list[PromptInput]:
    if message is None:
        return []
    if isinstance(message, PromptInput):
        if message.text.strip() or message.images:
            return [message]
        return []
    if isinstance(message, str):
        if message.strip():
            return [PromptInput(text=message)]
        return []
    if isinstance(message, Iterable):
        prompts: list[PromptInput] = []
        for item in message:
            if isinstance(item, PromptInput):
                if item.text.strip() or item.images:
                    prompts.append(item)
                continue
            if isinstance(item, str) and item.strip():
                prompts.append(PromptInput(text=item))
        return prompts
    return []


async def run_print_mode(
    session: SessionRuntime,
    message: str | PromptInput | Iterable[str | PromptInput] | None = None,
) -> int:
    prompt_list = _normalize_prompts(message)

    if prompt_list:
        for prompt in prompt_list:
            await session.prompt(prompt.text, images=prompt.images or None)
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
