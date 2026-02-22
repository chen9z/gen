from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

PaneFocus = Literal["left", "center", "right", "input"]
PickerMode = Literal["resume", "tree"]
LeftPaneSection = Literal["sessions", "tree", "tools"]

LIVE_CHAR_LIMIT = 8000


@dataclass
class LiveStreamState:
    text: str = ""
    thinking: str = ""
    toolcall: str = ""
    error: str | None = None
    max_chars: int = LIVE_CHAR_LIMIT


@dataclass
class PickerState:
    mode: PickerMode | None = None
    items: list[dict[str, Any]] = field(default_factory=list)
    selected_index: int = 0

    @property
    def is_open(self) -> bool:
        return self.mode is not None


@dataclass
class SelectionState:
    session_index: int = 0
    tree_index: int = 0
    tool_index: int = 0
    timeline_index: int = 0
    event_index: int = 0
    suggestion_index: int = 0


@dataclass
class UIState:
    focus: PaneFocus = "input"
    left_section: LeftPaneSection = "sessions"
    status_text: str = "Ready"
    meta_text: str = ""
    timeline_lines: list[str] = field(default_factory=list)
    event_lines: list[str] = field(default_factory=list)
    live: LiveStreamState = field(default_factory=LiveStreamState)
    picker: PickerState = field(default_factory=PickerState)
    selection: SelectionState = field(default_factory=SelectionState)
    input_history: list[str] = field(default_factory=list)
    history_cursor: int | None = None
    history_draft: str = ""
    command_suggestions: list[str] = field(default_factory=list)
