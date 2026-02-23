from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

WidgetPlacement = Literal["above_editor", "below_editor", "aboveEditor", "belowEditor"]
NotifyLevel = Literal["info", "warning", "error"]
WidgetContent = str | list[str] | None
HeaderFooterContent = str | list[str] | None


@dataclass
class CustomEditorComponent:
    """Text-only editor behavior hooks for interactive UIs."""

    placeholder: str | None = None
    title: str | None = None
    status_hint: str | None = None


EditorComponentInput = CustomEditorComponent | None


@runtime_checkable
class ExtensionUIContext(Protocol):
    async def select(self, title: str, options: list[str], timeout: int | None = None) -> str | None: ...

    async def confirm(
        self,
        title: str,
        message: str,
        timeout: int | None = None,
    ) -> bool: ...

    async def input(
        self,
        title: str,
        placeholder: str | None = None,
        timeout: int | None = None,
    ) -> str | None: ...

    async def editor(
        self,
        title: str,
        prefill: str | None = None,
        timeout: int | None = None,
    ) -> str | None: ...

    def notify(self, message: str, level: NotifyLevel = "info") -> None: ...

    def set_status(self, key: str, text: str | None) -> None: ...

    def set_widget(
        self,
        key: str,
        content: WidgetContent,
        placement: WidgetPlacement = "above_editor",
    ) -> None: ...

    def set_header(self, content: HeaderFooterContent) -> None: ...

    def set_footer(self, content: HeaderFooterContent) -> None: ...

    def set_title(self, title: str) -> None: ...

    def get_editor_text(self) -> str: ...

    def set_editor_text(self, text: str) -> None: ...

    def set_editor_component(self, component: EditorComponentInput) -> None: ...


class NoOpExtensionUIContext:
    async def select(self, title: str, options: list[str], timeout: int | None = None) -> str | None:
        del title, options, timeout
        return None

    async def confirm(self, title: str, message: str, timeout: int | None = None) -> bool:
        del title, message, timeout
        return False

    async def input(self, title: str, placeholder: str | None = None, timeout: int | None = None) -> str | None:
        del title, placeholder, timeout
        return None

    async def editor(self, title: str, prefill: str | None = None, timeout: int | None = None) -> str | None:
        del title, prefill, timeout
        return None

    def notify(self, message: str, level: NotifyLevel = "info") -> None:
        print(f"[{level.upper()}] {message}", file=sys.stderr)

    def set_status(self, key: str, text: str | None) -> None:
        del key, text

    def set_widget(
        self,
        key: str,
        content: WidgetContent,
        placement: WidgetPlacement = "above_editor",
    ) -> None:
        del key, content, placement

    def set_header(self, content: HeaderFooterContent) -> None:
        del content

    def set_footer(self, content: HeaderFooterContent) -> None:
        del content

    def set_title(self, title: str) -> None:
        del title

    def get_editor_text(self) -> str:
        return ""

    def set_editor_text(self, text: str) -> None:
        del text

    def set_editor_component(self, component: EditorComponentInput) -> None:
        del component

    # Compatibility aliases with pi naming.
    async def selectDialog(self, title: str, options: list[str], timeout: int | None = None) -> str | None:
        return await self.select(title, options, timeout=timeout)

    async def confirmDialog(self, title: str, message: str, timeout: int | None = None) -> bool:
        return await self.confirm(title, message, timeout=timeout)

    async def inputDialog(self, title: str, placeholder: str | None = None, timeout: int | None = None) -> str | None:
        return await self.input(title, placeholder=placeholder, timeout=timeout)

    def setStatus(self, key: str, text: str | None) -> None:
        self.set_status(key, text)

    def setWidget(
        self,
        key: str,
        content: WidgetContent,
        placement: WidgetPlacement = "aboveEditor",
    ) -> None:
        self.set_widget(key, content, placement=placement)

    def setHeader(self, content: HeaderFooterContent) -> None:
        self.set_header(content)

    def setFooter(self, content: HeaderFooterContent) -> None:
        self.set_footer(content)

    def setTitle(self, title: str) -> None:
        self.set_title(title)

    def getEditorText(self) -> str:
        return self.get_editor_text()

    def setEditorText(self, text: str) -> None:
        self.set_editor_text(text)

    def setEditorComponent(self, component: EditorComponentInput) -> None:
        self.set_editor_component(component)
