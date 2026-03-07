from __future__ import annotations

from rich.console import Console, RenderableType
from rich.live import Live


class RenderEngine:
    """Manages Rich Live instance lifecycle."""

    def __init__(self, console: Console):
        self._console = console
        self._live: Live | None = None

    @property
    def is_active(self) -> bool:
        return self._live is not None

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
        if self._live:
            self._live.stop()
            self._live = None

    def flush(self, renderable: RenderableType) -> None:
        if self._live is not None:
            self._live.update(renderable, refresh=True)
