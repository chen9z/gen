from __future__ import annotations

import asyncio
import time

from rich.console import Console, RenderableType
from rich.live import Live


class RenderEngine:
    """Manages Rich Live instance lifecycle and flush."""

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

    def flush(self, renderable: RenderableType) -> None:
        if self._live is not None:
            self._live.update(renderable, refresh=True)
            self._dirty = False
