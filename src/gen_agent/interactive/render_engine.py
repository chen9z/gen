from __future__ import annotations

import asyncio
import time

from rich.console import Console, Group, RenderableType
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

from .blocks import AssistantBlock, ToolRunBlock


class RenderEngine:
    """Manages rendering of the interactive UI.

    Handles Rich Live object lifecycle, renderable building,
    and adaptive refresh logic.
    """

    def __init__(self, console: Console, batch_interval: float = 0.04):
        self._console = console
        self._batch_interval = batch_interval

        self._live: Live | None = None
        self._flush_task: asyncio.Task[None] | None = None
        self._dirty = True

        # Adaptive refresh
        self._last_activity_time = time.monotonic()
        self._min_interval = 0.05  # 20Hz refresh rate
        self._max_interval = 0.2

    @property
    def console(self) -> Console:
        return self._console

    def start(self) -> None:
        """Start the live rendering."""
        if self._live is not None:
            return

        self._live = Live(
            Text(""),
            console=self._console,
            auto_refresh=False,
            transient=False,
            vertical_overflow="visible",
            redirect_stdout=False,
            redirect_stderr=False,
        )
        self._live.start()
        self._flush_task = asyncio.create_task(self._flush_loop())

    def stop(self) -> None:
        """Stop the live rendering."""
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None
        if self._live:
            self._live.stop()
            self._live = None

    def request_refresh(self) -> None:
        """Mark the view as dirty and request a refresh."""
        self._dirty = True
        self._last_activity_time = time.monotonic()

    def build_renderable(
        self,
        active_entries: list[AssistantBlock | ToolRunBlock],
        mooning_spinner: RenderableType | None,
        notices: list[tuple[str, str]],
        working: bool,
        current_turn: int,
        max_turns: int,
        widgets_above: dict[str, list[str]],
        widgets_below: dict[str, list[str]],
        has_entries: bool,
    ) -> RenderableType:
        """Build the renderable for the current state.

        Args:
            active_entries: Uncommitted entries to render
            mooning_spinner: Optional spinner to show
            notices: Active notices to display
            working: Whether currently working
            current_turn: Current turn number
            max_turns: Maximum turns
            widgets_above: Widgets to show above content
            widgets_below: Widgets to show below content
            has_entries: Whether there are any entries in the session

        Returns:
            Rich renderable for the current state
        """
        # Build content sections
        header_parts: list[RenderableType] = []
        main_parts: list[RenderableType] = []
        footer_parts: list[RenderableType] = []

        # Header: widgets above
        for _key, lines in sorted(widgets_above.items()):
            header_parts.extend(Text(line) for line in lines)

        # Main: active entries
        for entry in active_entries:
            main_parts.append(entry.render())

        if mooning_spinner is not None and not active_entries:
            main_parts.append(mooning_spinner)

        # Main: notices
        if notices:
            level, text = notices[-1]
            color = {"info": "dim", "warning": "yellow", "error": "red"}.get(level, "dim")
            main_parts.append(Text(f"  {text}", style=color))

        # Main: turn progress
        if working and current_turn > 0 and max_turns > 0:
            turn_text = Text(f"  Turn {current_turn}/{max_turns}", style="dim")
            main_parts.append(turn_text)

        # Footer: widgets below
        for _key, lines in sorted(widgets_below.items()):
            footer_parts.extend(Text(line) for line in lines)

        # Footer: keyboard hint
        if working:
            footer_parts.append(Text("  Ctrl+C to interrupt", style="dim"))

        # Use Layout if we have multiple sections, otherwise simple Group
        has_header = bool(header_parts)
        has_footer = bool(footer_parts)
        has_main = bool(main_parts)

        if not (has_header or has_footer or has_main):
            return Text("")

        # Simple case: only main content
        if not has_header and not has_footer:
            return Group(*main_parts) if main_parts else Text("")

        # Use Layout for structured layout
        layout = Layout()
        sections = []

        if has_header:
            sections.append(Layout(Group(*header_parts), name="header", size=len(header_parts)))

        if has_main:
            sections.append(Layout(Group(*main_parts), name="main"))

        if has_footer:
            sections.append(Layout(Group(*footer_parts), name="footer", size=len(footer_parts)))

        if len(sections) == 1:
            return sections[0].renderable

        layout.split_column(*sections)
        return layout

    def flush(self, renderable: RenderableType) -> None:
        """Flush the renderable to the live view."""
        if self._live is not None:
            self._live.update(renderable, refresh=True)

    async def _flush_loop(self) -> None:
        """Background task that periodically flushes the view."""
        while True:
            try:
                if self._dirty:
                    # Adaptive refresh rate based on activity
                    elapsed = time.monotonic() - self._last_activity_time
                    if elapsed < 1.0:
                        interval = self._min_interval
                    else:
                        interval = min(self._max_interval, self._min_interval + elapsed * 0.05)

                    await asyncio.sleep(interval)
                else:
                    await asyncio.sleep(self._batch_interval)
            except asyncio.CancelledError:
                break
