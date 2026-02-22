from __future__ import annotations

from typing import Any

__all__ = ["AgentSession", "SessionManager"]


def __getattr__(name: str) -> Any:
    if name == "AgentSession":
        from .agent_session import AgentSession

        return AgentSession
    if name == "SessionManager":
        from .session_manager import SessionManager

        return SessionManager
    raise AttributeError(name)
