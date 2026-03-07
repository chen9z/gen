from __future__ import annotations

from gen_agent.runtime import SessionRuntime


class AgentSession(SessionRuntime):
    """Backward-compatible shim for the legacy session entrypoint."""


__all__ = ["AgentSession"]
