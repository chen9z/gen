from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from gen_agent.core.agent_loop import run_agent_loop
from gen_agent.models.events import (
    AgentEnd,
    AssistantMessageEvent,
    AutoRetryEnd,
    AutoRetryStart,
    MessageEnd,
    MessageStart,
    MessageUpdate,
    TurnEnd,
)
from gen_agent.models.messages import AgentMessage, AssistantMessage


class RunExecutor:
    def __init__(
        self,
        *,
        provider_call: Callable[[list[AgentMessage]], Any],
        provider_stream_call: Callable[[list[AgentMessage]], Any],
        exec_tool: Callable[[str, dict[str, Any]], Any],
        emit: Callable[[Any], Any],
        event_emitter,
        get_steering_messages: Callable[[], list[AgentMessage]],
        get_follow_up_messages: Callable[[], list[AgentMessage]],
        provider_name_getter: Callable[[], str],
        model_id_getter: Callable[[], str],
        retry_settings_getter: Callable[[], Any],
    ) -> None:
        self._provider_call = provider_call
        self._provider_stream_call = provider_stream_call
        self._exec_tool = exec_tool
        self._emit = emit
        self._event_emitter = event_emitter
        self._get_steering_messages = get_steering_messages
        self._get_follow_up_messages = get_follow_up_messages
        self._provider_name_getter = provider_name_getter
        self._model_id_getter = model_id_getter
        self._retry_settings_getter = retry_settings_getter

    async def run(self, prompts: list[AgentMessage], context: list[AgentMessage]) -> list[AgentMessage]:
        retry = self._retry_settings_getter()
        attempt = 0
        max_retries = retry.max_retries if retry.enabled else 0
        self._event_emitter.begin_run()
        try:
            while True:
                try:
                    return await run_agent_loop(
                        prompts=prompts,
                        context_messages=context,
                        provider_call=self._provider_call,
                        exec_tool=self._exec_tool,
                        emit=self._emit,
                        provider_stream_call=self._provider_stream_call,
                        get_steering_messages=self._get_steering_messages,
                        get_follow_up_messages=self._get_follow_up_messages,
                        stream_provider=self._provider_name_getter(),
                        stream_model=self._model_id_getter(),
                    )
                except asyncio.CancelledError:
                    aborted = self._build_aborted_assistant()
                    self._emit_aborted_turn(aborted)
                    return [aborted]
                except Exception as exc:
                    if attempt >= max_retries:
                        self._emit(AutoRetryEnd(success=False, attempt=attempt, finalError=str(exc)))
                        raise
                    attempt += 1
                    delay = min(retry.base_delay_ms * (2 ** (attempt - 1)), retry.max_delay_ms)
                    self._emit(
                        AutoRetryStart(
                            attempt=attempt,
                            maxAttempts=max_retries,
                            delayMs=delay,
                            errorMessage=str(exc),
                        )
                    )
                    await asyncio.sleep(delay / 1000)
        finally:
            self._event_emitter.finish_run()

    def _build_aborted_assistant(self, message: str = "Request was aborted") -> AssistantMessage:
        return AssistantMessage(
            content=[],
            provider=self._provider_name_getter(),
            model=self._model_id_getter(),
            stopReason="aborted",
            errorMessage=message,
        )

    def _emit_aborted_turn(self, assistant: AssistantMessage) -> None:
        self._emit(MessageStart(message=assistant))
        self._emit(MessageUpdate(message=assistant, assistantMessageEvent=AssistantMessageEvent(type="start")))
        self._emit(
            MessageUpdate(
                message=assistant,
                assistantMessageEvent=AssistantMessageEvent(type="error", error=assistant.error_message or "aborted"),
            )
        )
        self._emit(MessageUpdate(message=assistant, assistantMessageEvent=AssistantMessageEvent(type="done")))
        self._emit(MessageEnd(message=assistant))
        self._emit(TurnEnd(message=assistant, toolResults=[]))
        self._emit(AgentEnd(messages=[assistant]))
