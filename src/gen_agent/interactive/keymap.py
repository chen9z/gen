from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import Protocol

from prompt_toolkit.key_binding import KeyBindings


class _InteractiveActions(Protocol):
    async def open_resume_picker(self) -> None: ...

    async def open_tree_picker(self) -> None: ...

    async def cycle_model(self, direction: str = "forward") -> None: ...

    async def new_session(self) -> None: ...

    async def manual_compact(self) -> None: ...

    async def toggle_status_detail(self) -> None: ...

    async def toggle_tool_details(self) -> None: ...



def _spawn(event, action: Awaitable[None]) -> None:
    creator = getattr(event.app, "create_background_task", None)
    if callable(creator):
        creator(action)
    else:
        asyncio.create_task(action)



def build_key_bindings(actions: _InteractiveActions) -> KeyBindings:
    kb = KeyBindings()

    @kb.add("c-r")
    def _resume(event) -> None:
        _spawn(event, actions.open_resume_picker())

    @kb.add("c-t")
    def _tree(event) -> None:
        _spawn(event, actions.open_tree_picker())

    @kb.add("c-l")
    def _cycle_next(event) -> None:
        _spawn(event, actions.cycle_model("forward"))

    @kb.add("c-p")
    def _cycle_prev(event) -> None:
        _spawn(event, actions.cycle_model("backward"))

    @kb.add("c-n")
    def _new_session(event) -> None:
        _spawn(event, actions.new_session())

    @kb.add("c-k")
    def _compact(event) -> None:
        _spawn(event, actions.manual_compact())

    @kb.add("c-y")
    def _toggle_status(event) -> None:
        _spawn(event, actions.toggle_status_detail())

    @kb.add("c-d")
    def _toggle_details(event) -> None:
        _spawn(event, actions.toggle_tool_details())

    return kb
