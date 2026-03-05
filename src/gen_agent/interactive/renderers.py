from __future__ import annotations

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from .data_models import AssistantData, ToolRunData
from .diff_renderer import extract_file_change_info, render_diff, summarize_diff
from .theme import Theme, DEFAULT_THEME


class AssistantRenderer:
    """Renders assistant message blocks."""

    def __init__(self, theme: Theme = DEFAULT_THEME):
        self.theme = theme

    def render(self, data: AssistantData, highlighter=None) -> RenderableType:
        """Render an assistant message block.

        Args:
            data: Assistant message data
            highlighter: Optional syntax highlighter for streaming

        Returns:
            Rich renderable
        """
        parts: list[RenderableType] = []

        if data.thinking:
            if data.done:
                parts.append(Text("Thinking...", style=self.theme.text_secondary))
            else:
                preview = self._single_line_preview(data.thinking, limit=80)
                parts.append(Text(f"Thinking: {preview}", style=self.theme.text_secondary))

        if data.text:
            if data.done:
                parts.append(Markdown(data.text))
            else:
                # Use streaming syntax highlighting if available
                if highlighter and highlighter.has_code_blocks():
                    highlighted = highlighter.render_highlighted()
                    parts.extend(highlighted)
                    parts.append(Text("▍"))
                else:
                    parts.append(Text(data.text + "▍"))
        elif not data.done and not data.thinking:
            parts.append(Spinner("dots", text="Thinking..."))

        if data.toolcalls:
            for _index, preview in sorted(data.toolcalls.items())[-2:]:
                name_preview = self._single_line_preview(preview.name, limit=48).strip() or "tool"
                args_preview = self._single_line_preview(preview.args, limit=96).strip()
                tc = Text()
                tc.append("> ", style=self.theme.info_color)
                tc.append(name_preview, style=self.theme.text_accent)
                if args_preview:
                    tc.append(f" ({args_preview})", style=self.theme.text_secondary)
                parts.append(tc)

        if data.error:
            parts.append(Text(f"Error: {data.error}", style=self.theme.error_color))

        if data.usage_text:
            parts.append(Text(data.usage_text, style=self.theme.text_secondary))

        return Group(*parts) if parts else Text("")

    @staticmethod
    def _single_line_preview(text: str, limit: int = 140) -> str:
        """Generate a single-line preview of text."""
        collapsed = " ".join(part for part in text.strip().split())
        if len(collapsed) <= limit:
            return collapsed
        return collapsed[: limit - 3] + "..."


class ToolRunRenderer:
    """Renders tool execution blocks."""

    def __init__(self, theme: Theme = DEFAULT_THEME):
        self.theme = theme

    def render(
        self,
        data: ToolRunData,
        show_details: bool = False,
        show_diff: bool = False,
    ) -> RenderableType:
        """Render a tool execution block.

        Args:
            data: Tool execution data
            show_details: Whether to show error details
            show_diff: Whether to show diff

        Returns:
            Rich renderable
        """
        key_arg = self._extract_key_arg(data.name, data.args)

        if data.status == "running":
            label = Text()
            label.append(data.name, style=self.theme.text_accent)
            if key_arg:
                label.append(f": {key_arg}", style=self.theme.text_secondary)
            return Spinner("dots", text=label)

        line = Text()
        if data.is_error:
            line.append("x ", style=self.theme.error_color)
        else:
            line.append("✓ ", style=self.theme.success_color)
        line.append(data.name, style=self.theme.text_accent)
        if key_arg:
            line.append(f": {key_arg}", style=self.theme.text_secondary)
        if data.duration > 0.1:
            line.append(f" ({data.duration:.2f}s)", style=self.theme.text_secondary)

        # Add diff summary for file changes
        if not data.is_error and data.result:
            change_info = extract_file_change_info(data.name, data.args, data.result)
            if change_info:
                file_path, old_content, new_content = change_info
                diff_summary = summarize_diff(old_content, new_content)
                line.append(f" [{diff_summary}]", style=f"{self.theme.info_color} dim")

        if data.result_summary:
            line.append(f" - {data.result_summary}", style=self.theme.text_secondary)

        # Add visual indicators for expandable content
        if data.is_error and data.error_detail:
            indicator = "▼" if show_details else "▶"
            line.append(f" {indicator}", style=self.theme.text_secondary)
        elif not data.is_error and data.result:
            change_info = extract_file_change_info(data.name, data.args, data.result)
            if change_info:
                indicator = "▼" if show_diff else "▶"
                line.append(f" {indicator}", style=self.theme.text_secondary)

        parts = [line]

        # Show error details if available and expanded
        if data.is_error and data.error_detail and show_details:
            detail_text = Text(data.error_detail, style=f"{self.theme.error_color} dim")
            parts.append(Panel(detail_text, title="Error Details", border_style=self.theme.error_color))

        # Show diff if available and expanded
        if not data.is_error and show_diff and data.result:
            change_info = extract_file_change_info(data.name, data.args, data.result)
            if change_info:
                file_path, old_content, new_content = change_info
                diff_view = render_diff(old_content, new_content, file_path)
                parts.append(Panel(diff_view, title=f"Diff: {file_path}", border_style=self.theme.info_color))

        return Group(*parts) if len(parts) > 1 else line

    @staticmethod
    def _extract_key_arg(name: str, args: dict) -> str:
        """Extract the key argument for display."""
        _TOOL_KEY_ARGS = {
            "Read": ["path"],
            "Write": ["path"],
            "Edit": ["path"],
            "Bash": ["command"],
            "Grep": ["pattern", "path"],
            "Find": ["pattern", "path"],
            "Ls": ["path"],
        }
        keys = _TOOL_KEY_ARGS.get(name, [])
        for key in keys:
            value = args.get(key)
            if isinstance(value, str) and value.strip():
                return value[:60] + "..." if len(value) > 60 else value
        for value in args.values():
            if isinstance(value, str) and value.strip():
                return value[:60] + "..." if len(value) > 60 else value
        return ""
