from __future__ import annotations

import asyncio
import signal
import sys
import time
from collections.abc import Iterable
from typing import Any

from gen_agent.extensions import CustomEditorComponent, NoOpExtensionUIContext
from gen_agent.models.events import AgentSessionEvent
from gen_agent.models.messages import AssistantMessage
from gen_agent.runtime import SessionRuntime

from .blocks import LIVE_CHAR_LIMIT
from .dialogs import create_confirm_dialog, create_input_dialog, run_with_timeout
from .keymap import build_key_bindings
from .live_view import LiveView
from .pickers import choose_from_values, choose_session, choose_tree
from .prompt_session import InteractivePromptSession

_BUILTIN_COMMANDS = [
    "quit",
    "new",
    "reload",
    "model",
    "name",
    "session",
    "hotkeys",
    "settings",
    "compact",
    "tree",
    "fork",
    "resume",
    "scoped-models",
]


def _normalize_lines(content: Any, *, field_name: str) -> list[str] | None:
    if content is None:
        return None
    if isinstance(content, str):
        return content.splitlines() or [content]
    if isinstance(content, list):
        if not all(isinstance(line, str) for line in content):
            raise TypeError(f"{field_name} only supports str | list[str] | None")
        return list(content)
    raise TypeError(f"{field_name} only supports str | list[str] | None")


def _normalize_widget_placement(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"beloweditor", "below_editor"}:
        return "below_editor"
    return "above_editor"


class PtkExtensionUIContext:
    def __init__(self, app: "GenInteractiveApp") -> None:
        self._app = app

    async def select(self, title: str, options: list[str], timeout: int | None = None) -> str | None:
        values = [(option, option) for option in options]
        return await choose_from_values(title, "Select an option", values, timeout_ms=timeout)

    async def confirm(self, title: str, message: str, timeout: int | None = None) -> bool:
        task = create_confirm_dialog(title=title, text=message).run_async()
        return bool(await run_with_timeout(task, timeout))

    async def input(self, title: str, placeholder: str | None = None, timeout: int | None = None) -> str | None:
        task = create_input_dialog(
            title=title,
            text=placeholder or "Enter value",
            default=self._app.get_editor_text(),
        ).run_async()
        return await run_with_timeout(task, timeout)

    async def editor(self, title: str, prefill: str | None = None, timeout: int | None = None) -> str | None:
        task = create_input_dialog(
            title=title,
            text="Edit text and confirm",
            default=prefill or self._app.get_editor_text(),
        ).run_async()
        return await run_with_timeout(task, timeout)

    def notify(self, message: str, level: str = "info") -> None:
        self._app.notify(message, level=level)

    def set_status(self, key: str, text: str | None) -> None:
        self._app.set_status(key, text)

    def set_widget(self, key: str, content: Any, placement: Any = "above_editor") -> None:
        lines = _normalize_lines(content, field_name="set_widget content")
        placement_token = _normalize_widget_placement(str(placement))
        self._app.set_widget(key, lines, placement=placement_token)

    def set_header(self, content: Any) -> None:
        self._app.set_header(_normalize_lines(content, field_name="set_header content"))

    def set_footer(self, content: Any) -> None:
        self._app.set_footer(_normalize_lines(content, field_name="set_footer content"))

    def set_title(self, title: str) -> None:
        self._app.set_title(title)

    def get_editor_text(self) -> str:
        return self._app.get_editor_text()

    def set_editor_text(self, text: str) -> None:
        self._app.set_editor_text(text)

    def set_editor_component(self, component: Any) -> None:
        if component is not None and not isinstance(component, CustomEditorComponent):
            raise TypeError("set_editor_component only accepts CustomEditorComponent | None")
        self._app.set_editor_component(component)

    async def selectDialog(self, title: str, options: list[str], timeout: int | None = None) -> str | None:
        return await self.select(title, options, timeout=timeout)

    async def confirmDialog(self, title: str, message: str, timeout: int | None = None) -> bool:
        return await self.confirm(title, message, timeout=timeout)

    async def inputDialog(self, title: str, placeholder: str | None = None, timeout: int | None = None) -> str | None:
        return await self.input(title, placeholder=placeholder, timeout=timeout)

    def setStatus(self, key: str, text: str | None) -> None:
        self.set_status(key, text)

    def setWidget(self, key: str, content: Any, placement: Any = "aboveEditor") -> None:
        if isinstance(placement, dict):
            placement = placement.get("placement", "aboveEditor")
        self.set_widget(key, content, placement=placement)

    def setHeader(self, content: Any) -> None:
        self.set_header(content)

    def setFooter(self, content: Any) -> None:
        self.set_footer(content)

    def setTitle(self, title: str) -> None:
        self.set_title(title)

    def getEditorText(self) -> str:
        return self.get_editor_text()

    def setEditorText(self, text: str) -> None:
        self.set_editor_text(text)

    def setEditorComponent(self, component: Any) -> None:
        self.set_editor_component(component)


class GenInteractiveApp:
    def __init__(self, session: SessionRuntime, initial_prompt: str | None = None):
        self.session = session
        self.initial_prompt = initial_prompt
        self._session_unsub = None
        self._run_lock = asyncio.Lock()
        self._active_run_task: asyncio.Task[list[Any]] | None = None
        self._previous_sigint_handler: Any | None = None

        self._editor_text = ""
        self._editor_component: CustomEditorComponent | None = None
        self._last_interrupt_time: float = 0.0
        self._force_quit = False

        self._live_view = LiveView(session)
        self._prompt_session = InteractivePromptSession(
            cwd=session.cwd,
            command_provider=self.command_pool,
            key_bindings=build_key_bindings(self),
            toolbar_provider=self._live_view.build_input_toolbar,
        )

    def command_pool(self) -> list[str]:
        ext = sorted(self.session.extension_runner.get_commands().keys())
        seen = set()
        ordered: list[str] = []
        for item in [*_BUILTIN_COMMANDS, *ext]:
            if item in seen:
                continue
            seen.add(item)
            ordered.append(item)
        return ordered

    def notify(self, message: str, level: str = "info") -> None:
        self._live_view.add_notice(message, level=level)

    def set_status(self, key: str, text: str | None) -> None:
        self._live_view.set_status(key, text)

    def set_widget(self, key: str, lines: list[str] | None, placement: str = "above_editor") -> None:
        self._live_view.set_widget(key, lines, placement=placement)

    def set_header(self, lines: list[str] | None) -> None:
        self._live_view.set_header(lines)

    def set_footer(self, lines: list[str] | None) -> None:
        self._live_view.set_footer(lines)

    def set_title(self, title: str) -> None:
        self._live_view.set_title(title)

    def get_editor_text(self) -> str:
        return self._editor_text

    def set_editor_text(self, text: str) -> None:
        self._editor_text = text

    def set_editor_component(self, component: CustomEditorComponent | None) -> None:
        self._editor_component = component
        if component and component.status_hint:
            self._live_view.set_status("editor", component.status_hint)
        else:
            self._live_view.set_status("editor", None)

    def _editor_prompt_prefix(self) -> str:
        if self._editor_component and self._editor_component.placeholder:
            return f"› {self._editor_component.placeholder}: "
        return "› "

    def _cancel_active_run(self) -> None:
        now = time.monotonic()
        task = self._active_run_task
        if task is None or task.done():
            self._last_interrupt_time = now
            return
        if self._last_interrupt_time > 0 and now - self._last_interrupt_time < 1.5:
            self._force_quit = True
            task.cancel()
            self._live_view.add_notice("Force quit", level="warning")
            return
        task.cancel()
        self._last_interrupt_time = now
        self._live_view._toolcall_phase.clear()
        self._live_view.add_notice("Interrupted (Ctrl+C again to quit)", level="warning")

    def _install_sigint_handler(self) -> None:
        if self._previous_sigint_handler is not None:
            return
        try:
            loop = asyncio.get_running_loop()
            self._previous_sigint_handler = signal.getsignal(signal.SIGINT)

            def _handler(_signum: int, _frame: Any) -> None:
                loop.call_soon_threadsafe(self._cancel_active_run)

            signal.signal(signal.SIGINT, _handler)
        except (RuntimeError, ValueError):
            self._previous_sigint_handler = None

    def _restore_sigint_handler(self) -> None:
        if self._previous_sigint_handler is None:
            return
        signal.signal(signal.SIGINT, self._previous_sigint_handler)
        self._previous_sigint_handler = None

    def _on_session_event(self, event: AgentSessionEvent) -> None:
        self._live_view.on_session_event(event)

    def _append_assistant_messages(self, messages: Iterable[Any]) -> None:
        for message in messages:
            if isinstance(message, AssistantMessage):
                self._live_view.add_assistant_message(message)

    async def _submit(self, text: str, *, echo_user: bool = True) -> bool:
        payload = text.strip()
        if not payload:
            return True
        if payload == "/quit":
            return False
        async with self._run_lock:
            self._prompt_session.record_submission(payload)
            if echo_user:
                self._live_view.print_user_prompt(payload)
            self._force_quit = False
            self._live_view.clear_input_usage_text()
            self._live_view.start()
            try:
                stream_tick = self._live_view.stream_tick
                self._active_run_task = asyncio.create_task(self.session.prompt(payload))
                self._install_sigint_handler()
                try:
                    result = await self._active_run_task
                except SystemExit:
                    return False
                except asyncio.CancelledError:
                    return not self._force_quit
                except Exception as exc:
                    self._live_view.add_notice(f"error: {exc}", level="error")
                    return True
                finally:
                    self._active_run_task = None
                    self._restore_sigint_handler()

                if self._live_view.stream_tick == stream_tick:
                    self._append_assistant_messages(result)
                return True
            finally:
                self._live_view.stop()
                self._editor_text = ""

    async def open_resume_picker(self) -> None:
        selected = await choose_session(self.session)
        if not selected:
            return
        path = self.session.resume_session(selected)
        self._live_view.add_notice(f"Resumed: {path}", level="info")

    async def open_tree_picker(self) -> None:
        selected = await choose_tree(self.session)
        if selected is None:
            return
        leaf_id = None if selected == "__root__" else selected
        ok = self.session.switch_tree(leaf_id)
        if ok:
            target = leaf_id or "root"
            self._live_view.add_notice(f"Tree switched: {target}", level="info")
        else:
            self._live_view.add_notice(f"Unknown tree leaf: {selected}", level="error")

    async def cycle_model(self, direction: str = "forward") -> None:
        data = self.session.cycle_model(direction=direction)
        self._live_view.add_notice(
            f"Model: {data.get('provider')}/{data.get('modelId')} thinking={data.get('thinkingLevel')}",
            level="info",
        )

    async def new_session(self) -> None:
        self.session.new_session()
        self._live_view.add_notice("Started new session", level="info")

    async def manual_compact(self) -> None:
        await self._submit("/compact", echo_user=False)

    async def toggle_tool_details(self) -> None:
        self._live_view.toggle_last_tool_details()

    async def run_async(self) -> int:
        if self.session.ui_extensions_enabled:
            self.session.bind_ui_context(PtkExtensionUIContext(self))
        else:
            self.session.bind_ui_context(NoOpExtensionUIContext())

        self._session_unsub = self.session.subscribe(self._on_session_event)
        try:
            self._live_view.print_welcome_banner()

            if self.initial_prompt:
                self._live_view.print_user_prompt(self.initial_prompt)
                keep_running = await self._submit(self.initial_prompt, echo_user=False)
                if not keep_running:
                    return 0

            while True:
                try:
                    text = await self._prompt_session.prompt_async(
                        self._editor_prompt_prefix(),
                        default=self._editor_text,
                    )
                except EOFError:
                    break
                except KeyboardInterrupt:
                    continue
                finally:
                    self._editor_text = ""

                keep_running = await self._submit(text, echo_user=False)
                if not keep_running:
                    break
        finally:
            if self._session_unsub:
                self._session_unsub()
            self.session.bind_ui_context(NoOpExtensionUIContext())
            self._live_view.stop()
        return 0


async def run_interactive_mode(session: SessionRuntime, initial_message: str | None = None) -> int:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        from gen_agent.modes.print_mode import run_print_mode

        return await run_print_mode(session, initial_message)
    app = GenInteractiveApp(session=session, initial_prompt=initial_message)
    return await app.run_async()


__all__ = ["GenInteractiveApp", "LIVE_CHAR_LIMIT", "PtkExtensionUIContext", "run_interactive_mode"]
