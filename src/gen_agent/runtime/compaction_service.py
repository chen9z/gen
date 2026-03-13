from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from gen_agent.core.compaction import (
    build_compaction_message,
    estimate_message_tokens,
    generate_compaction_summary,
    should_compact,
)

if TYPE_CHECKING:
    from gen_agent.core.session_manager import SessionManager
    from gen_agent.models.settings import CompactionSettings


@dataclass
class AutoCompactionResult:
    applied: bool
    reason: str | None = None
    summary: str | None = None
    estimated_tokens: int | None = None


class CompactionService:
    def __init__(
        self,
        *,
        session_manager: "SessionManager",
        settings_getter: Callable[[], "CompactionSettings"],
    ) -> None:
        self._session_manager = session_manager
        self._settings_getter = settings_getter

    def maybe_auto_compact(self) -> AutoCompactionResult:
        settings = self._settings_getter()
        context = self._session_manager.build_context().messages
        compaction = should_compact(
            context,
            reserve_tokens=settings.reserve_tokens,
            keep_recent_tokens=settings.keep_recent_tokens,
        )
        if not settings.enabled or not compaction.should_compact or not self._session_manager.entries:
            return AutoCompactionResult(applied=False)
        summary = self._apply_compaction(context, compaction.estimated_tokens)
        return AutoCompactionResult(
            applied=True,
            reason=compaction.reason or "threshold",
            summary=summary,
            estimated_tokens=compaction.estimated_tokens,
        )

    def compact_now(self) -> str:
        context = self._session_manager.build_context().messages
        if not context or not self._session_manager.entries:
            return "No session context to compact."
        summary = generate_compaction_summary(context)
        self._apply_compaction(context, len(summary) // 4)
        return "Manual compaction completed."

    def _apply_compaction(self, context, estimated_tokens: int) -> str:
        summary = generate_compaction_summary(context)
        keep_recent_tokens = self._settings_getter().keep_recent_tokens
        first_kept_entry_id = self._select_anchor_id(keep_recent_tokens)
        self._session_manager.append_compaction(summary, first_kept_entry_id, estimated_tokens)
        compact_msg = build_compaction_message(summary, estimated_tokens)
        self._session_manager.append_message(compact_msg)
        return summary

    def _select_anchor_id(self, keep_recent_tokens: int) -> str:
        branch = self._session_manager.get_branch()
        if not branch:
            return self._session_manager.entries[max(0, len(self._session_manager.entries) // 2)].id

        budget = max(1, keep_recent_tokens)
        running = 0
        anchor = branch[0].id
        for entry in reversed(branch):
            anchor = entry.id
            if entry.type == "message":
                running += estimate_message_tokens([entry.message])
            elif entry.type in {"branch_summary", "compaction"}:
                running += max(1, len(entry.summary) // 4)
            elif entry.type == "custom":
                running += max(1, len(str(getattr(entry, "data", ""))) // 4)
            if running >= budget:
                break
        return anchor
