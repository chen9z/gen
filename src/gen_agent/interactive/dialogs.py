from __future__ import annotations

import asyncio
from typing import TypeVar

from prompt_toolkit.shortcuts import input_dialog, radiolist_dialog, yes_no_dialog
from prompt_toolkit.styles import Style

_DIALOG_STYLE = Style.from_dict(
    {
        "dialog": "bg:#111827",
        "dialog frame.label": "bold #f3f4f6",
        "dialog.body": "bg:#111827 #d1d5db",
        "dialog shadow": "bg:#030712",
        "button": "bg:#1f2937 #d1d5db",
        "button.focused": "bg:#2563eb #ffffff",
        "radio": "#9ca3af",
        "radio.focused": "#ffffff",
        "radio-selected": "#60a5fa",
        "text-area": "bg:#0f172a #e5e7eb",
        "text-area.focused": "bg:#0f172a #ffffff",
    }
)

T = TypeVar("T")


async def run_with_timeout(task: asyncio.Future[T], timeout_ms: int | None = None) -> T | None:
    if timeout_ms and timeout_ms > 0:
        try:
            return await asyncio.wait_for(task, timeout=timeout_ms / 1000)
        except asyncio.TimeoutError:
            return None
    return await task


def create_select_dialog(title: str, text: str, values: list[tuple[str, str]]):
    return radiolist_dialog(
        title=title,
        text=text,
        values=values,
        ok_text="Select",
        cancel_text="Cancel",
        style=_DIALOG_STYLE,
    )


def create_confirm_dialog(title: str, text: str):
    return yes_no_dialog(
        title=title,
        text=text,
        yes_text="Confirm",
        no_text="Cancel",
        style=_DIALOG_STYLE,
    )


def create_input_dialog(title: str, text: str, *, default: str = ""):
    return input_dialog(
        title=title,
        text=text,
        default=default,
        ok_text="Confirm",
        cancel_text="Cancel",
        style=_DIALOG_STYLE,
    )
