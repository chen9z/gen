from __future__ import annotations

from rich.panel import Panel
from rich.text import Text

from gen_agent.core.agent_session import AgentSession

from .render import InteractiveRenderState


def build_status_line(session: AgentSession, state: InteractiveRenderState, editor_title: str | None = None) -> Text:
    meta = session.get_state()
    session_name = meta.get("sessionName") or "-"
    pending = meta.get("pendingMessageCount", 0)
    thinking = meta.get("thinkingLevel", "off")
    provider = meta.get("provider", "-")
    model_id = meta.get("modelId", "-")
    editor = f" | editor={editor_title}" if editor_title else ""
    return Text(
        f"provider={provider}/{model_id} | thinking={thinking} | session={session_name} | pending={pending} | status={state.status_text}{editor}"
    )


def build_text_panel(title: str, lines: list[str] | None, *, style: str = "") -> Panel:
    body = "\n".join(lines or ["-"])
    return Panel(body, title=title, border_style=style or "cyan")
