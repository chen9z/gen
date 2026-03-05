from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.application.current import get_app_or_none
from prompt_toolkit.buffer import Buffer, CompletionState
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase, merge_key_bindings
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style

from .completers import AtPathCompleter, HybridCompleter, SlashFuzzyCompleter
from .history import HistoryStore


def accept_completion_or_submit(buffer: Buffer) -> bool:
    state = buffer.complete_state
    if not isinstance(state, CompletionState):
        return False
    completion = state.current_completion
    if completion is None and state.completions:
        completion = state.completions[0]
    if completion is None:
        return False
    buffer.apply_completion(completion)
    buffer.complete_state = None
    return True


def insert_newline(buffer: Buffer) -> None:
    buffer.insert_text("\n")


def build_input_key_bindings(base_bindings: KeyBindingsBase | None = None) -> KeyBindingsBase:
    kb = KeyBindings()

    @kb.add("c-j")
    def _newline_ctrl_j(event) -> None:
        insert_newline(event.current_buffer)

    @kb.add("escape", "enter")
    def _newline_alt_enter(event) -> None:
        insert_newline(event.current_buffer)

    @kb.add("enter", eager=True)
    def _accept_or_submit(event) -> None:
        if accept_completion_or_submit(event.current_buffer):
            return
        event.current_buffer.validate_and_handle()

    bindings: list[KeyBindingsBase] = [kb]
    if base_bindings is not None:
        bindings.insert(0, base_bindings)
    return merge_key_bindings(bindings)


class InteractivePromptSession:
    def __init__(
        self,
        *,
        cwd: str,
        command_provider: Callable[[], Sequence[str]],
        key_bindings: KeyBindingsBase | None = None,
    ) -> None:
        self._history_store = HistoryStore(cwd)
        self._history = InMemoryHistory()
        for entry in self._history_store.load():
            self._history.append_string(entry)

        completer = HybridCompleter(
            SlashFuzzyCompleter(command_provider),
            AtPathCompleter(Path(cwd)),
        )
        merged_bindings = build_input_key_bindings(key_bindings)
        style = Style.from_dict(
            {
                "completion-menu": "bg:#1f2430 #d5def5",
                "completion-menu.completion.current": "bg:#2f67d8 #ffffff",
                "completion-menu.meta.completion.current": "bg:#2f67d8 #ffffff",
                # Remove default reverse-video on bottom toolbar so it blends
                # with the terminal background instead of showing a white bar.
                "bottom-toolbar": "noreverse",
                "bottom-toolbar.text": "#555555",
            }
        )
        self._session = PromptSession(
            history=self._history,
            completer=completer,
            complete_while_typing=True,
            complete_style=CompleteStyle.MULTI_COLUMN,
            reserve_space_for_menu=0,
            key_bindings=merged_bindings,
            enable_history_search=True,
            prompt_continuation="  ",
            style=style,
        )

    async def prompt_async(self, prompt: str, *, default: str = "") -> str:
        return await self._session.prompt_async(
            prompt, default=default, bottom_toolbar=self._bottom_toolbar,
        )

    @staticmethod
    def _bottom_toolbar() -> str:
        app = get_app_or_none()
        cols = 80
        if app is not None:
            try:
                cols = int(app.output.get_size().columns)
            except Exception:
                pass
        return "─" * max(cols, 1)

    def record_submission(self, text: str) -> None:
        self._history_store.append(text)
