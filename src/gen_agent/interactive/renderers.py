from __future__ import annotations

from rich.console import Group, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from .data_models import AssistantData, ToolRunData
from .diff_renderer import extract_file_change_info, render_diff, summarize_diff
from .theme import Theme, DEFAULT_THEME
from .tool_key_args import extract_key_arg_from_json, extract_tool_key_arg, normalize_tool_name


class AssistantRenderer:
    """Renders assistant message blocks."""

    def __init__(self, theme: Theme = DEFAULT_THEME):
        self.theme = theme

    def render(self, data: AssistantData, highlighter=None) -> RenderableType:
        parts: list[RenderableType] = []

        # Only show thinking spinner when streaming and no text yet
        if data.thinking and not data.done and not data.text:
            parts.append(Spinner("dots", text="Thinking...", style=self.theme.text_secondary))

        if data.text:
            if data.done:
                parts.append(Markdown(data.text))
            else:
                if highlighter and highlighter.has_code_blocks():
                    highlighted = highlighter.render_highlighted()
                    parts.extend(highlighted)
                    parts.append(Text("▍"))
                else:
                    parts.append(Text(data.text + "▍"))
        elif not data.done and not data.thinking:
            parts.append(Spinner("dots", text="Thinking...", style=self.theme.text_secondary))

        # Only show toolcall preview during streaming
        if data.toolcalls and not data.done:
            preview = sorted(data.toolcalls.items())[-1][1]  # only last one
            name = preview.name.strip()
            if name:
                key_arg = extract_key_arg_from_json(name, preview.args)
                tc = Text()
                tc.append("  ⏺ ", style=f"dim {self.theme.info_color}")
                tc.append(normalize_tool_name(name), style=self.theme.text_accent)
                if key_arg:
                    tc.append(f" {key_arg}", style=self.theme.text_secondary)
                parts.append(tc)

        if data.error:
            parts.append(Text(f"Error: {data.error}", style=self.theme.error_color))

        if data.usage_text and data.done:
            parts.append(Text(data.usage_text, style=self.theme.text_secondary))

        return Group(*parts) if parts else Text("")


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
        key_arg = extract_tool_key_arg(data.name, data.args)
        display_name = normalize_tool_name(data.name)

        if data.status == "running":
            label = Text()
            label.append(f"  {display_name}", style=self.theme.text_accent)
            if key_arg:
                label.append(f" {key_arg}", style=self.theme.text_secondary)
            return Spinner("dots", text=label)

        line = Text()
        if data.is_error:
            line.append("  ✗ ", style=self.theme.error_color)
        else:
            line.append("  ✓ ", style=self.theme.success_color)
        line.append(display_name, style=self.theme.text_accent)
        if key_arg:
            line.append(f" {key_arg}", style=self.theme.text_secondary)
        if data.duration > 0.1:
            line.append(f" ({data.duration:.2f}s)", style=self.theme.text_secondary)

        # Compute change_info once, reuse below
        change_info = None
        if not data.is_error and data.result:
            change_info = extract_file_change_info(data.name, data.args, data.result)
            if change_info:
                file_path, old_content, new_content = change_info
                diff_summary = summarize_diff(old_content, new_content)
                line.append(f" [{diff_summary}]", style=f"{self.theme.info_color} dim")

        if data.is_error and data.result_summary:
            line.append(f" - {data.result_summary}", style=self.theme.text_secondary)

        # Add visual indicators for expandable content
        if data.is_error and data.error_detail:
            indicator = "▼" if show_details else "▶"
            line.append(f" {indicator}", style=self.theme.text_secondary)
        elif change_info is not None:
            indicator = "▼" if show_diff else "▶"
            line.append(f" {indicator}", style=self.theme.text_secondary)

        parts: list[RenderableType] = [line]

        # Show error details if available and expanded
        if data.is_error and data.error_detail and show_details:
            detail_text = Text(data.error_detail, style=f"{self.theme.error_color} dim")
            parts.append(Panel(detail_text, title="Error Details", border_style=self.theme.error_color))

        # Show diff if available and expanded
        if not data.is_error and show_diff and change_info:
            file_path, old_content, new_content = change_info
            diff_view = render_diff(old_content, new_content, file_path)
            parts.append(Panel(diff_view, title=f"Diff: {file_path}", border_style=self.theme.info_color))

        return Group(*parts) if len(parts) > 1 else line
