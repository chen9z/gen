from __future__ import annotations

import difflib
from typing import Any

from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text


def render_diff(old_content: str, new_content: str, file_path: str = "", side_by_side: bool = False) -> RenderableType:
    """Render a diff with syntax highlighting.

    Args:
        old_content: Original file content
        new_content: Modified file content
        file_path: Optional file path for context
        side_by_side: If True, render side-by-side columns; otherwise unified diff

    Returns:
        Rich renderable showing the diff with color coding
    """
    if side_by_side:
        return _render_side_by_side_diff(old_content, new_content)

    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{file_path}" if file_path else "original",
            tofile=f"b/{file_path}" if file_path else "modified",
            lineterm="",
        )
    )

    if not diff_lines:
        return Text("No changes", style="dim")

    # Build colored diff output
    parts: list[Text] = []
    for line in diff_lines:
        text = Text(line)
        if line.startswith("+++") or line.startswith("---"):
            text.stylize("bold")
        elif line.startswith("+"):
            text.stylize("green")
        elif line.startswith("-"):
            text.stylize("red")
        elif line.startswith("@@"):
            text.stylize("cyan")
        parts.append(text)

    return Group(*parts)


def _render_side_by_side_diff(old_content: str, new_content: str) -> RenderableType:
    """Render a side-by-side diff using Columns.

    Args:
        old_content: Original file content
        new_content: Modified file content

    Returns:
        Rich Columns showing old and new content side by side
    """
    old_text = Text(old_content or "(empty)", style="red dim")
    new_text = Text(new_content or "(empty)", style="green dim")

    old_panel = Panel(old_text, title="Before", border_style="red", padding=(0, 1))
    new_panel = Panel(new_text, title="After", border_style="green", padding=(0, 1))

    return Columns([old_panel, new_panel], equal=True, expand=True)


def summarize_diff(old_content: str, new_content: str) -> str:
    """Generate a brief summary of changes.

    Args:
        old_content: Original file content
        new_content: Modified file content

    Returns:
        Brief summary like "+5 -3 lines"
    """
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            lineterm="",
        )
    )

    additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))

    if additions == 0 and deletions == 0:
        return "no changes"

    parts = []
    if additions > 0:
        parts.append(f"+{additions}")
    if deletions > 0:
        parts.append(f"-{deletions}")

    return " ".join(parts) + " lines"


def extract_file_change_info(tool_name: str, args: dict[str, Any], result: Any) -> tuple[str, str, str] | None:
    """Extract file change information from tool execution.

    Args:
        tool_name: Name of the tool (Edit, Write, etc.)
        args: Tool arguments
        result: Tool execution result

    Returns:
        Tuple of (file_path, old_content, new_content) or None if not applicable
    """
    if tool_name not in ("Edit", "Write"):
        return None

    file_path = args.get("file_path") or args.get("path", "")
    if not file_path:
        return None

    # For Write tool, we don't have old content in most cases
    if tool_name == "Write":
        # Check if result contains old content (for overwrites)
        if isinstance(result, dict):
            old_content = result.get("old_content", "")
            new_content = args.get("content", "")
            if old_content or new_content:
                return (file_path, old_content, new_content)
        return None

    # For Edit tool
    if tool_name == "Edit":
        old_string = args.get("old_string", "")
        new_string = args.get("new_string", "")
        if old_string or new_string:
            # Return a simplified diff context
            return (file_path, old_string, new_string)

    return None
