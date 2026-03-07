from __future__ import annotations

from typing import Any

from rich.spinner import Spinner

from .blocks import AssistantBlock, ToolRunBlock, UserPromptBlock


class StateManager:
    """Manages the state of the interactive UI."""

    def __init__(self, entry_limit: int = 240):
        self._entry_limit = entry_limit
        self._entries: list[UserPromptBlock | AssistantBlock | ToolRunBlock] = []
        self._tool_runs: dict[str, ToolRunBlock] = {}
        self._draft: AssistantBlock | None = None
        self._active_toolcall_index: int | None = None
        self._toolcall_phase: dict[int, str] = {}
        self._sticky_error_notice: str | None = None
        self._working = False
        self._mooning_spinner: Spinner | None = None
        self._committed_count = 0
        self._current_usage: dict[str, Any] = {"input": 0, "output": 0, "cost": 0.0}
        self._current_turn = 0
        self._max_turns = 0

    def get_entries(self) -> list[UserPromptBlock | AssistantBlock | ToolRunBlock]:
        return self._entries

    def get_active_entries(self) -> list[UserPromptBlock | AssistantBlock | ToolRunBlock]:
        return self._entries

    def append_entry(self, entry: UserPromptBlock | AssistantBlock | ToolRunBlock) -> None:
        self._entries.append(entry)
        if len(self._entries) <= self._entry_limit:
            return

        removed = self._entries.pop(0)
        if removed is self._draft:
            self._draft = None
        if isinstance(removed, ToolRunBlock):
            self._tool_runs.pop(removed.tool_call_id, None)
        elif isinstance(removed, AssistantBlock):
            for content_index in list(removed.toolcalls.keys()):
                self._toolcall_phase.pop(content_index, None)

    def get_draft(self) -> AssistantBlock | None:
        return self._draft

    def set_draft(self, draft: AssistantBlock | None) -> None:
        self._draft = draft

    def get_tool_run(self, tool_call_id: str) -> ToolRunBlock | None:
        return self._tool_runs.get(tool_call_id)

    def set_tool_run(self, tool_call_id: str, block: ToolRunBlock) -> None:
        self._tool_runs[tool_call_id] = block

    def get_active_toolcall_index(self) -> int | None:
        return self._active_toolcall_index

    def set_active_toolcall_index(self, index: int | None) -> None:
        self._active_toolcall_index = index

    def get_toolcall_phase(self, content_index: int) -> str | None:
        return self._toolcall_phase.get(content_index)

    def set_toolcall_phase(self, content_index: int, phase: str) -> None:
        self._toolcall_phase[content_index] = phase

    def clear_toolcall_phases(self) -> None:
        self._toolcall_phase.clear()

    def get_sticky_error_notice(self) -> str | None:
        return self._sticky_error_notice

    def set_sticky_error_notice(self, notice: str | None) -> None:
        self._sticky_error_notice = notice

    def is_working(self) -> bool:
        return self._working

    def set_working(self, working: bool) -> None:
        self._working = working

    def get_mooning_spinner(self) -> Spinner | None:
        return self._mooning_spinner

    def set_mooning_spinner(self, spinner: Spinner | None) -> None:
        self._mooning_spinner = spinner

    def get_committed_count(self) -> int:
        return self._committed_count

    def set_committed_count(self, count: int) -> None:
        self._committed_count = count

    def increment_committed_count(self, delta: int = 1) -> None:
        self._committed_count += delta

    def get_current_usage(self) -> dict[str, Any]:
        return self._current_usage

    def update_usage(self, input_tokens: int = 0, output_tokens: int = 0, cost: float = 0.0) -> None:
        self._current_usage["input"] += input_tokens
        self._current_usage["output"] += output_tokens
        self._current_usage["cost"] += cost

    def reset_usage(self) -> None:
        self._current_usage = {"input": 0, "output": 0, "cost": 0.0}

    def get_turn_progress(self) -> tuple[int, int]:
        return (self._current_turn, self._max_turns)

    def set_turn_progress(self, current: int, max_turns: int) -> None:
        self._current_turn = current
        self._max_turns = max_turns

    def reset_turn_progress(self) -> None:
        self._current_turn = 0
        self._max_turns = 0
