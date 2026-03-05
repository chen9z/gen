from __future__ import annotations

from rich.console import Console

from .blocks import AssistantBlock, ToolRunBlock


class CommitManager:
    """Manages the commit/rollback of entries in the live view.

    Handles the logic for determining when entries should be committed
    (scrolled off the live view) and manages the committed count.
    """

    def __init__(self, console: Console):
        self._console = console

    def commit_ready_entries(
        self,
        entries: list[AssistantBlock | ToolRunBlock],
        committed_count: int,
    ) -> int:
        """Commit entries that are ready to be scrolled off.

        Args:
            entries: All entries in the live view
            committed_count: Current number of committed entries

        Returns:
            New committed count after committing ready entries
        """
        if committed_count >= len(entries):
            return committed_count

        # Find entries that are ready to commit (completed and stable)
        new_committed = committed_count
        for i in range(committed_count, len(entries)):
            entry = entries[i]

            # Commit completed assistant blocks
            if isinstance(entry, AssistantBlock) and entry.done:
                new_committed = i + 1
                continue

            # Commit completed tool runs
            if isinstance(entry, ToolRunBlock) and entry.status == "done":
                new_committed = i + 1
                continue

            # Stop at first non-ready entry
            break

        # Print newly committed entries to console
        if new_committed > committed_count:
            for i in range(committed_count, new_committed):
                self._console.print(entries[i].render())

        return new_committed
