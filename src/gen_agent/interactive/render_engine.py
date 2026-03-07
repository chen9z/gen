from __future__ import annotations

import asyncio
import time

from rich.console import Console, Group, RenderableType
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

from .blocks import AssistantBlock, ToolRunBlock


class RenderEngine:
    """Manages rendering of the interactive UI."""

    def __init__(self, console: Console, batch_interval: float = 0.04):
        self._console = console
        self._batch_interval = batch_interval
        self._live: Live | None = None
        self._flush_task: asyncio.Task[None] | None = None
        self._dirty = True
        self._last_activity_time = time.monotonic()
        self._min_interval = 0.05
        self._max_interval = 0.2

    @property
    def console(self) -> Console:
        return self._console

    def start(self) -> None:
        if self._live is not None:
            return
        self._live = Live(
            Text(""),
            console=self._console,
            auto_refresh=False,
            transient=True,
            vertical_overflow="visible",
            redirect_stdout=False,
            redirect_stderr=False,
        )
        self._live.start()

    def stop(self) -> None:
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None
        if self._live:
            self._live.stop()
            self._live = None

    def request_refresh(self) -> None:
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
        header_parts: list[RenderableType] = []
        main_parts: list[RenderableType] = []
        footer_parts: list[RenderableType] = []

        for _key, lines in sorted(widgets_above.items()):
            header_parts.extend(Text(line) for line in lines)

        for entry in active_entries:
            main_parts.append(entry.render())

        if mooning_spinner is not None and not active_entries and not has_entries:
            main_parts.append(mooning_spinner)

        if notices:
            level, text = notices[-1]
            color = {"info": "dim", "warning": "yellow", "error": "red"}.get(level, "dim")
            footer_parts.append(Text(f"  {text}", style=color))

        if working and current_turn > 0 and max_turns > 0:
            footer_parts.append(Text(f"  Turn {current_turn}/{max_turns}", style="dim"))

        for _key, lines in sorted(widgets_below.items()):
            footer_parts.extend(Text(line) for line in lines)

        if working:
            footer_parts.append(Text("  Ctrl+C to interrupt", style="dim"))

        has_header = bool(header_parts)
        has_footer = bool(footer_parts)
        has_main = bool(main_parts)
        if not (has_header or has_footer or has_main):
            return Text("")
        if not has_header and not has_footer:
            return Group(*main_parts) if main_parts else Text("")

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
        if self._live is not None:
            self._live.update(renderable, refresh=True)
            self._dirty = False

    async def _flush_loop(self) -> None:
        while True:
            try:
                if self._dirty:
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
