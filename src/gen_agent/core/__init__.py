from __future__ import annotations

from typing import Any

__all__ = ["AgentSession", "SessionManager", "SessionRuntime"]


def __getattr__(name: str) -> Any:
    if name == "AgentSession":
        from .agent_session import AgentSession

        return AgentSession
    if name == "SessionManager":
        from .session_manager import SessionManager

        return SessionManager
    if name == "SessionRuntime":
        from gen_agent.runtime import SessionRuntime

        return SessionRuntime
    raise AttributeError(name)
