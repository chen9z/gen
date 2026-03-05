from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.text import Text


def get_shortcuts_info() -> list[tuple[str, str]]:
    """Get list of keyboard shortcuts and their descriptions.

    Returns:
        List of (key, description) tuples
    """
    return [
        ("Ctrl+R", "Open session picker (resume)"),
        ("Ctrl+T", "Open tree/branch picker"),
        ("Ctrl+L", "Cycle model forward"),
        ("Ctrl+P", "Cycle model backward"),
        ("Ctrl+N", "Start new session"),
        ("Ctrl+K", "Manual compaction"),
        ("Ctrl+Y", "Toggle status detail view"),
        ("Ctrl+J", "Insert newline (in input)"),
        ("Alt+Enter", "Insert newline (in input)"),
        ("Tab", "Fuzzy completion (/ commands, @ paths)"),
        ("Up/Down", "Navigate input history"),
        ("Esc", "Cancel picker/dialog"),
    ]


def render_shortcuts_table() -> Table:
    """Render keyboard shortcuts as a Rich table.

    Returns:
        Rich Table with shortcuts
    """
    table = Table(title="Keyboard Shortcuts", show_header=True, header_style="bold cyan")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Action", style="white")

    for key, description in get_shortcuts_info():
        table.add_row(key, description)

    return table


def print_shortcuts(console: Console | None = None) -> None:
    """Print keyboard shortcuts to console.

    Args:
        console: Optional Rich console instance
    """
    if console is None:
        console = Console()

    table = render_shortcuts_table()
    console.print()
    console.print(table)
    console.print()
    console.print(
        Text("Tip: Use /help for more commands", style="dim italic"),
    )
    console.print()


def get_shortcuts_summary() -> str:
    """Get a brief summary of key shortcuts for status display.

    Returns:
        Brief summary string
    """
    return "Ctrl+R=resume | Ctrl+T=tree | Ctrl+L/P=model | Ctrl+N=new | Ctrl+K=compact"
