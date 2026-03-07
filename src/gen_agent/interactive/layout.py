from __future__ import annotations

from rich.panel import Panel
from rich.text import Text

from gen_agent.core.agent_session import AgentSession

from .render import InteractiveRenderState


def build_status_line(
    session: AgentSession,
    state: InteractiveRenderState,
    editor_title: str | None = None,
    current_turn: int = 0,
    max_turns: int = 0,
    *,
    detail: bool = False,
    status_items: dict[str, str] | None = None,
) -> Text:
    _ = state
    meta = session.get_state()
    provider = meta.get("provider", "-")
    model_id = meta.get("modelId", "-")
    thinking = meta.get("thinkingLevel", "off")

    parts = [f"{provider}/{model_id}"]
    if editor_title:
        parts.append(editor_title)
    if detail and thinking != "off":
        parts.append(f"thinking={thinking}")
    if detail and current_turn > 0 and max_turns > 0:
        parts.append(f"turn {current_turn}/{max_turns}")
    if detail and status_items:
        parts.extend(status_items.values())
    return Text(" · ".join(parts), style="dim")


def build_text_panel(title: str, lines: list[str] | None, *, style: str = "") -> Panel:
    body = "\n".join(lines or ["-"])
    return Panel(body, title=title, border_style=style or "cyan")
