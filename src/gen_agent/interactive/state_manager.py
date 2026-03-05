from __future__ import annotations

from typing import Any

from rich.spinner import Spinner

from .blocks import AssistantBlock, ToolRunBlock


class StateManager:
    """Manages the state of the interactive UI.

    Centralizes state management for entries, tool runs, usage tracking,
    and turn progress. Provides query interfaces for accessing state.
    """

    def __init__(self, entry_limit: int = 240):
        self._entry_limit = entry_limit

        # Entry management
        self._entries: list[AssistantBlock | ToolRunBlock] = []
        self._tool_runs: dict[str, ToolRunBlock] = {}
        self._draft: AssistantBlock | None = None
        self._active_toolcall_index: int | None = None
        self._toolcall_phase: dict[int, str] = {}

        # UI state
        self._sticky_error_notice: str | None = None
        self._working = False
        self._mooning_spinner: Spinner | None = None

        # Commit tracking
        self._committed_count = 0

        # Usage tracking
        self._current_usage: dict[str, Any] = {"input": 0, "output": 0, "cost": 0.0}

        # Turn progress
        self._current_turn = 0
        self._max_turns = 0

    # ------------------------------------------------------------------
    # Entry management
    # ------------------------------------------------------------------

    def get_entries(self) -> list[AssistantBlock | ToolRunBlock]:
        """Get all entries."""
        return self._entries

    def get_active_entries(self) -> list[AssistantBlock | ToolRunBlock]:
        """Get uncommitted entries."""
        return self._entries[self._committed_count:]

    def append_entry(self, entry: AssistantBlock | ToolRunBlock) -> None:
        """Append an entry and enforce entry limit."""
        self._entries.append(entry)
        if len(self._entries) <= self._entry_limit:
            return

        # Remove oldest entry
        removed = self._entries.pop(0)
        if self._committed_count > 0:
            self._committed_count -= 1
        if removed is self._draft:
            self._draft = None
        if isinstance(removed, ToolRunBlock):
            self._tool_runs.pop(removed.tool_call_id, None)
        elif isinstance(removed, AssistantBlock):
            # Clean up toolcall phase tracking for removed assistant block
            for content_index in list(removed.toolcalls.keys()):
                self._toolcall_phase.pop(content_index, None)

    def get_draft(self) -> AssistantBlock | None:
        """Get the current draft block."""
        return self._draft

    def set_draft(self, draft: AssistantBlock | None) -> None:
        """Set the current draft block."""
        self._draft = draft

    def get_tool_run(self, tool_call_id: str) -> ToolRunBlock | None:
        """Get a tool run by ID."""
        return self._tool_runs.get(tool_call_id)

    def set_tool_run(self, tool_call_id: str, block: ToolRunBlock) -> None:
        """Register a tool run."""
        self._tool_runs[tool_call_id] = block

    def get_active_toolcall_index(self) -> int | None:
        """Get the active toolcall index."""
        return self._active_toolcall_index

    def set_active_toolcall_index(self, index: int | None) -> None:
        """Set the active toolcall index."""
        self._active_toolcall_index = index

    def get_toolcall_phase(self, content_index: int) -> str | None:
        """Get the phase of a toolcall."""
        return self._toolcall_phase.get(content_index)

    def set_toolcall_phase(self, content_index: int, phase: str) -> None:
        """Set the phase of a toolcall."""
        self._toolcall_phase[content_index] = phase

    def clear_toolcall_phases(self) -> None:
        """Clear all toolcall phases."""
        self._toolcall_phase.clear()

    # ------------------------------------------------------------------
    # UI state
    # ------------------------------------------------------------------

    def get_sticky_error_notice(self) -> str | None:
        """Get the sticky error notice."""
        return self._sticky_error_notice

    def set_sticky_error_notice(self, notice: str | None) -> None:
        """Set the sticky error notice."""
        self._sticky_error_notice = notice

    def is_working(self) -> bool:
        """Check if currently working."""
        return self._working

    def set_working(self, working: bool) -> None:
        """Set working state."""
        self._working = working

    def get_mooning_spinner(self) -> Spinner | None:
        """Get the mooning spinner."""
        return self._mooning_spinner

    def set_mooning_spinner(self, spinner: Spinner | None) -> None:
        """Set the mooning spinner."""
        self._mooning_spinner = spinner

    # ------------------------------------------------------------------
    # Commit tracking
    # ------------------------------------------------------------------

    def get_committed_count(self) -> int:
        """Get the number of committed entries."""
        return self._committed_count

    def set_committed_count(self, count: int) -> None:
        """Set the number of committed entries."""
        self._committed_count = count

    def increment_committed_count(self, delta: int = 1) -> None:
        """Increment the committed count."""
        self._committed_count += delta

    # ------------------------------------------------------------------
    # Usage tracking
    # ------------------------------------------------------------------

    def get_current_usage(self) -> dict[str, Any]:
        """Get current usage statistics."""
        return self._current_usage

    def update_usage(self, input_tokens: int = 0, output_tokens: int = 0, cost: float = 0.0) -> None:
        """Update usage statistics."""
        self._current_usage["input"] += input_tokens
        self._current_usage["output"] += output_tokens
        self._current_usage["cost"] += cost

    def reset_usage(self) -> None:
        """Reset usage statistics."""
        self._current_usage = {"input": 0, "output": 0, "cost": 0.0}

    # ------------------------------------------------------------------
    # Turn progress
    # ------------------------------------------------------------------

    def get_turn_progress(self) -> tuple[int, int]:
        """Get current turn and max turns."""
        return (self._current_turn, self._max_turns)

    def set_turn_progress(self, current: int, max_turns: int) -> None:
        """Set turn progress."""
        self._current_turn = current
        self._max_turns = max_turns

    def reset_turn_progress(self) -> None:
        """Reset turn progress."""
        self._current_turn = 0
        self._max_turns = 0
