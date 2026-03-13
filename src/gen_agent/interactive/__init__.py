"""Interactive mode — minimal REPL with streaming output."""

from __future__ import annotations

import sys
from typing import Any

from rich.console import Console

from .app import InteractiveApp
from .stream_view import StreamView


async def run_interactive_mode(
    session: Any,
    initial_message: str | None = None,
) -> int:
    """Entry point for interactive mode.

    Falls back to print mode when stdin/stdout are not TTYs.
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        from gen_agent.modes.print_mode import run_print_mode

        return await run_print_mode(session, initial_message)

    console = Console()
    app = InteractiveApp(session, console)
    return await app.run(initial_message=initial_message)


__all__ = ["InteractiveApp", "StreamView", "run_interactive_mode"]
