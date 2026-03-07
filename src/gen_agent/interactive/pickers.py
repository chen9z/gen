from __future__ import annotations

from typing import Any

from gen_agent.core.agent_session import AgentSession

from .dialogs import create_select_dialog, run_with_timeout


def _tree_label(entry: dict[str, Any], index: int, current_leaf: str | None) -> str:
    marker = "*" if entry.get("id") == current_leaf else " "
    eid = entry.get("id") or "root"
    etype = entry.get("type") or "unknown"
    return f"{marker} {index + 1:02d}. {eid} ({etype})"


async def choose_from_values(
    title: str,
    text: str,
    values: list[tuple[str, str]],
    timeout_ms: int | None = None,
) -> str | None:
    if not values:
        return None
    dialog = create_select_dialog(title=title, text=text, values=values)
    return await run_with_timeout(dialog.run_async(), timeout_ms)


async def choose_session(session: AgentSession) -> str | None:
    sessions = session.list_sessions(limit=30, include_current=False)
    values = [
        (
            row["path"],
            f"{idx}. {row.get('name') or row.get('firstMessage') or '(no title)'} | messages={row.get('messageCount', 0)}\\n{row['path']}",
        )
        for idx, row in enumerate(sessions, start=1)
    ]
    return await choose_from_values("Resume Session", "Select a previous session", values)


async def choose_tree(session: AgentSession) -> str | None:
    tree = session.get_tree(limit=80, include_root=True)
    entries = tree.get("entries", [])
    leaf_id = tree.get("leafId")
    values: list[tuple[str, str]] = []
    for idx, entry in enumerate(entries):
        entry_id = entry.get("id")
        value = "__root__" if entry_id is None else str(entry_id)
        values.append((value, _tree_label(entry, idx, leaf_id)))
    return await choose_from_values("Switch Tree", "Select context branch", values)
