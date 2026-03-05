from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Theme:
    """Theme configuration for interactive UI styling."""

    # Status colors
    success_color: str = "green"
    error_color: str = "red"
    warning_color: str = "yellow"
    info_color: str = "cyan"

    # Text colors
    text_primary: str = "white"
    text_secondary: str = "dim"
    text_accent: str = "bold"
    text_muted: str = "bright_black"

    # UI colors
    border_color: str = "bright_black"
    spinner_color: str = "cyan"
    progress_color: str = "cyan"

    # Syntax highlighting
    code_theme: str = "monokai"

    # Tool execution colors
    tool_running_color: str = "cyan"
    tool_success_color: str = "green"
    tool_error_color: str = "red"


# Default theme (current style)
DEFAULT_THEME = Theme()

# Dark theme variant
DARK_THEME = Theme(
    success_color="green",
    error_color="red",
    warning_color="yellow",
    info_color="blue",
    text_primary="white",
    text_secondary="dim",
    text_accent="bold cyan",
    text_muted="bright_black",
    border_color="bright_black",
    spinner_color="blue",
    progress_color="blue",
    code_theme="monokai",
    tool_running_color="blue",
    tool_success_color="green",
    tool_error_color="red",
)

# High contrast theme for accessibility
HIGH_CONTRAST_THEME = Theme(
    success_color="bright_green",
    error_color="bright_red",
    warning_color="bright_yellow",
    info_color="bright_cyan",
    text_primary="bright_white",
    text_secondary="white",
    text_accent="bold bright_white",
    text_muted="white",
    border_color="white",
    spinner_color="bright_cyan",
    progress_color="bright_cyan",
    code_theme="monokai",
    tool_running_color="bright_cyan",
    tool_success_color="bright_green",
    tool_error_color="bright_red",
)
