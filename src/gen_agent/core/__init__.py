from __future__ import annotations

from typing import Any

__all__ = ["SessionManager"]


def __getattr__(name: str) -> Any:
    if name == "SessionManager":
        from .session_manager import SessionManager

        return SessionManager
    raise AttributeError(name)
