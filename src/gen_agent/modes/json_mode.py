from __future__ import annotations

import sys
from collections.abc import Iterable

import orjson

from gen_agent.models.prompt import PromptInput
from gen_agent.runtime import SessionRuntime


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


async def run_json_mode(
    session: SessionRuntime,
    message: str | PromptInput | Iterable[str | PromptInput] | None = None,
) -> int:
    header = session.session_manager.header
    if header:
        sys.stdout.write(orjson.dumps(header.model_dump(by_alias=True)).decode("utf-8") + "\n")

    def on_event(event):
        sys.stdout.write(orjson.dumps(event.model_dump(by_alias=True)).decode("utf-8") + "\n")
        sys.stdout.flush()

    unsub = session.subscribe(on_event)
    try:
        prompts = _normalize_prompts(message)
        if prompts:
            for prompt in prompts:
                await session.prompt(prompt.text, images=prompt.images or None)
        else:
            await session.continue_run()
    finally:
        unsub()
    last_assistant = next((m for m in reversed(session.get_messages()) if getattr(m, "role", "") == "assistant"), None)
    if last_assistant and getattr(last_assistant, "stop_reason", "") in {"error", "aborted"}:
        return 1
    return 0
