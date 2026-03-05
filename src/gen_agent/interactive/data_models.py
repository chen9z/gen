from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolcallData:
    """Pure data model for a toolcall preview."""

    name: str = ""
    args: str = ""


@dataclass
class AssistantData:
    """Pure data model for assistant message content."""

    text: str = ""
    thinking: str = ""
    toolcalls: dict[int, ToolcallData] = field(default_factory=dict)
    error: str | None = None
    done: bool = False
    usage_text: str = ""


@dataclass
class ToolRunData:
    """Pure data model for tool execution."""

    tool_call_id: str
    name: str
    args: dict[str, Any]
    status: str = "running"  # "running" | "done"
    is_error: bool = False
    result: Any = None
    result_summary: str | None = None
    error_detail: str | None = None
    start_time: float = 0.0
    duration: float = 0.0
