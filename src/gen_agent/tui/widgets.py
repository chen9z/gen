from __future__ import annotations

from typing import Any

from .state import UIState


def _mark(selected: bool) -> str:
    return ">" if selected else " "


def render_left_panel(
    state: UIState,
    sessions: list[dict[str, Any]],
    tree_entries: list[dict[str, Any]],
    tools: list[str],
) -> str:
    lines: list[str] = ["[Left Pane]"]
    lines.append("")
    session_header = "Sessions"
    if state.focus == "left" and state.left_section == "sessions":
        session_header += " [active]"
    lines.append(session_header)
    for idx, item in enumerate(sessions[:9], start=1):
        selected = (
            (state.picker.is_open and state.picker.mode == "resume" and state.picker.selected_index == idx - 1)
            or (
                not state.picker.is_open
                and state.focus == "left"
                and state.left_section == "sessions"
                and state.selection.session_index == idx - 1
            )
        )
        title = str(item.get("name") or item.get("firstMessage") or "(no title)")
        lines.append(f"{_mark(selected)} {idx}. {title}")

    lines.append("")
    tree_header = "Tree"
    if state.focus == "left" and state.left_section == "tree":
        tree_header += " [active]"
    lines.append(tree_header)
    preview_tree = tree_entries[-8:] if len(tree_entries) > 8 else tree_entries
    for idx, item in enumerate(preview_tree, start=1):
        token = "root" if item.get("id") is None else str(item.get("id"))
        selected = state.focus == "left" and state.left_section == "tree" and state.selection.tree_index == idx - 1
        lines.append(f"{_mark(selected)} {idx}. {token}")

    lines.append("")
    tools_header = "Tools"
    if state.focus == "left" and state.left_section == "tools":
        tools_header += " [active]"
    lines.append(tools_header)
    for idx, tool in enumerate(tools[:10], start=1):
        selected = state.focus == "left" and state.left_section == "tools" and state.selection.tool_index == idx - 1
        lines.append(f"{_mark(selected)} {idx}. {tool}")
    return "\n".join(lines)


def render_live_panel(state: UIState) -> str:
    if state.picker.is_open:
        mode = state.picker.mode or ""
        lines = [f"[{mode.upper()} PICKER] Use Up/Down or 1-9, Enter to confirm, Esc to cancel"]
        for idx, item in enumerate(state.picker.items[:20], start=1):
            selected = state.picker.selected_index == idx - 1
            mark = _mark(selected)
            if mode == "resume":
                title = str(item.get("name") or item.get("firstMessage") or "(no title)")
                lines.append(f"{mark} {idx}. {title} | {item.get('path')}")
            else:
                token = "root" if item.get("id") is None else str(item.get("id"))
                lines.append(f"{mark} {idx}. {token} | type={item.get('type')}")
        return "\n".join(lines)

    parts: list[str] = []
    if state.live.text:
        parts.append(f"Gen (streaming):\n{state.live.text}")
    if state.live.thinking:
        parts.append(f"Thinking:\n{state.live.thinking}")
    if state.live.toolcall:
        parts.append(f"Tool call:\n{state.live.toolcall}")
    if state.live.error:
        parts.append(f"[error] {state.live.error}")
    return "\n\n".join(parts)


def render_inspector(
    state: UIState,
    current_session_file: str | None,
    sessions: list[dict[str, Any]],
    tree_entries: list[dict[str, Any]],
    tools: list[str],
) -> str:
    def _short(text: str, limit: int = 100) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 1] + "…"

    lines: list[str] = ["[Inspector]"]
    lines.append("")
    lines.append(f"Focus: {state.focus}")
    lines.append(f"Status: {state.status_text}")
    lines.append(f"Session file: {current_session_file or '-'}")
    lines.append("")

    lines.append("Selection")
    lines.append(f"- Left section: {state.left_section}")
    session_idx = state.selection.session_index
    tree_idx = state.selection.tree_index
    tool_idx = state.selection.tool_index
    timeline_idx = state.selection.timeline_index
    event_idx = state.selection.event_index

    if sessions:
        s_idx = min(max(0, session_idx), len(sessions) - 1)
        item = sessions[s_idx]
        title = str(item.get("name") or item.get("firstMessage") or "(no title)")
        lines.append(f"- Session[{s_idx + 1}]: {_short(title)}")
    if tree_entries:
        t_idx = min(max(0, tree_idx), len(tree_entries) - 1)
        token = "root" if tree_entries[t_idx].get("id") is None else str(tree_entries[t_idx].get("id"))
        lines.append(f"- Tree[{t_idx + 1}]: {_short(token)}")
    if tools:
        o_idx = min(max(0, tool_idx), len(tools) - 1)
        lines.append(f"- Tool[{o_idx + 1}]: {_short(tools[o_idx])}")
    if state.timeline_lines:
        l_idx = min(max(0, timeline_idx), len(state.timeline_lines) - 1)
        lines.append(f"- Timeline[{l_idx + 1}]: {_short(state.timeline_lines[l_idx])}")
    if state.event_lines:
        e_idx = min(max(0, event_idx), len(state.event_lines) - 1)
        lines.append(f"- Event[{e_idx + 1}]: {_short(state.event_lines[e_idx])}")
    lines.append("")

    if state.command_suggestions:
        lines.append("Command Suggestions")
        for idx, item in enumerate(state.command_suggestions, start=1):
            selected = state.selection.suggestion_index == idx - 1
            lines.append(f"{_mark(selected)} {idx}. {item}")
        lines.append("")

    if state.event_lines:
        lines.append("Recent Events")
        start = max(0, len(state.event_lines) - 12)
        for idx, line in enumerate(state.event_lines[start:], start=start):
            selected = idx == min(max(0, state.selection.event_index), len(state.event_lines) - 1)
            lines.append(f"{_mark(selected)} {_short(line)}")
    return "\n".join(lines)
