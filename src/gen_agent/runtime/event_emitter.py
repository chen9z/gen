from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import uuid4

from gen_agent.models.events import AgentEvent, AgentSessionEvent

if TYPE_CHECKING:
    from .session_runtime import SessionRuntime


class EventEmitter:
    def __init__(self, runtime: "SessionRuntime") -> None:
        self._runtime = runtime
        self._listeners: list[Callable[[AgentSessionEvent], None]] = []
        self._run_id: str | None = None
        self._actor_id = "main"
        self._parent_run_id: str | None = None

    def subscribe(self, listener: Callable[[AgentSessionEvent], None]) -> Callable[[], None]:
        self._listeners.append(listener)

        def _unsubscribe() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return _unsubscribe

    def begin_run(self, *, parent_run_id: str | None = None, actor_id: str = "main") -> str:
        self._run_id = uuid4().hex
        self._parent_run_id = parent_run_id
        self._actor_id = actor_id
        return self._run_id

    def finish_run(self) -> None:
        self._run_id = None
        self._parent_run_id = None
        self._actor_id = "main"

    def emit(self, event: AgentSessionEvent | AgentEvent) -> AgentSessionEvent:
        enriched = self._with_envelope(event)
        event_type = getattr(enriched, "type", "")
        if event_type:
            try:
                payload = (
                    enriched.model_dump(by_alias=True)
                    if hasattr(enriched, "model_dump")
                    else {"type": event_type}
                )
                self._runtime.extension_runner.emit(event_type, payload, self._runtime)
            except Exception:
                pass
        for listener in list(self._listeners):
            listener(enriched)
        return enriched

    def _with_envelope(self, event: AgentSessionEvent | AgentEvent) -> AgentSessionEvent:
        header = self._runtime.session_manager.header
        return event.model_copy(
            update={
                "run_id": self._run_id,
                "actor_id": self._actor_id,
                "parent_run_id": self._parent_run_id,
                "session_id": header.id if header else None,
            }
        )
