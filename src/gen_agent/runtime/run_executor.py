from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from gen_agent.core.agent_loop import run_agent_loop
from gen_agent.models.events import AutoRetryEnd, AutoRetryStart
from gen_agent.models.messages import AgentMessage

if TYPE_CHECKING:
    from .session_runtime import SessionRuntime


class RunExecutor:
    def __init__(self, runtime: "SessionRuntime") -> None:
        self._runtime = runtime

    async def run(self, prompts: list[AgentMessage], context: list[AgentMessage]) -> list[AgentMessage]:
        retry = self._runtime.settings.retry
        attempt = 0
        max_retries = retry.max_retries if retry.enabled else 0
        self._runtime.event_emitter.begin_run()
        try:
            while True:
                try:
                    return await run_agent_loop(
                        prompts=prompts,
                        context_messages=context,
                        provider_call=self._runtime._provider_call,
                        exec_tool=self._runtime._execute_tool,
                        emit=self._runtime._emit,
                        provider_stream_call=self._runtime._provider_stream_call,
                        get_steering_messages=self._runtime._dequeue_steering,
                        get_follow_up_messages=self._runtime._dequeue_follow_up,
                        stream_provider=self._runtime.provider_name,
                        stream_model=self._runtime.model_id,
                    )
                except asyncio.CancelledError:
                    aborted = self._runtime._build_aborted_assistant()
                    self._runtime._emit_aborted_turn(aborted)
                    return [aborted]
                except Exception as exc:
                    if attempt >= max_retries:
                        self._runtime._emit(AutoRetryEnd(success=False, attempt=attempt, finalError=str(exc)))
                        raise
                    attempt += 1
                    delay = min(retry.base_delay_ms * (2 ** (attempt - 1)), retry.max_delay_ms)
                    self._runtime._emit(
                        AutoRetryStart(
                            attempt=attempt,
                            maxAttempts=max_retries,
                            delayMs=delay,
                            errorMessage=str(exc),
                        )
                    )
                    await asyncio.sleep(delay / 1000)
        finally:
            self._runtime.event_emitter.finish_run()
