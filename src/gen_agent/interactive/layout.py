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
) -> Text:
    meta = session.get_state()
    provider = meta.get("provider", "-")
    model_id = meta.get("modelId", "-")
    thinking = meta.get("thinkingLevel", "off")
    turn_info = f" · turn {current_turn}/{max_turns}" if current_turn > 0 and max_turns > 0 else ""
    parts = f"{provider}/{model_id}"
    if thinking != "off":
        parts += f" · thinking={thinking}"
    parts += turn_info
    if editor_title:
        parts += f" · {editor_title}"
    return Text(parts, style="dim")


def build_text_panel(title: str, lines: list[str] | None, *, style: str = "") -> Panel:
    body = "\n".join(lines or ["-"])
    return Panel(body, title=title, border_style=style or "cyan")
