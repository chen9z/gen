from __future__ import annotations

from collections.abc import Callable, Sequence
from html import escape
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.application.current import get_app_or_none
from prompt_toolkit.buffer import Buffer, CompletionState
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase, merge_key_bindings
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style
from wcwidth import wcswidth

from .completers import AtPathCompleter, HybridCompleter, SlashFuzzyCompleter
from .history import HistoryStore

_HINT_REQUIRED_TOKENS = ("Enter send", "Esc+Enter newline", "Ctrl+C interrupt")
_HINT_OPTIONAL_TOKENS = ("/ commands", "@ files", "Ctrl+R resume")
_HINT_SEPARATOR = " · "


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
        status_provider: Callable[[], str],
        key_bindings: KeyBindingsBase | None = None,
    ) -> None:
        self._status_provider = status_provider
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
                "bottom-toolbar": "fg:#8f95a8",
            }
        )
        self._session = PromptSession(
            history=self._history,
            completer=completer,
            complete_while_typing=True,
            complete_style=CompleteStyle.MULTI_COLUMN,
            reserve_space_for_menu=8,
            key_bindings=merged_bindings,
            enable_history_search=True,
            prompt_continuation="  ",
            style=style,
        )

    async def prompt_async(self, prompt: str, *, default: str = "") -> str:
        return await self._session.prompt_async(
            prompt,
            default=default,
            bottom_toolbar=self._bottom_toolbar,
        )

    def record_submission(self, text: str) -> None:
        self._history_store.append(text)

    @staticmethod
    def _toolbar_columns() -> int:
        app = get_app_or_none()
        if app is None:
            return 80
        try:
            columns = int(app.output.get_size().columns)
        except Exception:
            return 80
        return columns if columns > 0 else 80

    @staticmethod
    def _display_width(text: str) -> int:
        width = wcswidth(text)
        return width if width >= 0 else len(text)

    def _truncate_with_ellipsis(self, text: str, limit: int) -> str:
        if self._display_width(text) <= limit:
            return text
        if limit <= 3:
            # Keep behavior predictable for tiny terminals.
            return text[:limit]
        target = limit - 3
        buf: list[str] = []
        width = 0
        for ch in text:
            w = self._display_width(ch)
            if width + w > target:
                break
            buf.append(ch)
            width += w
        return "".join(buf) + "..."

    def _join_hint_tokens(self, tokens: Sequence[str]) -> str:
        return _HINT_SEPARATOR.join(tokens)

    def _compose_toolbar_hint(self, columns: int) -> str:
        full_tokens = [*_HINT_REQUIRED_TOKENS, *_HINT_OPTIONAL_TOKENS]
        full_text = self._join_hint_tokens(full_tokens)
        if self._display_width(full_text) <= columns:
            return full_text

        tokens = list(_HINT_REQUIRED_TOKENS)
        for token in _HINT_OPTIONAL_TOKENS:
            candidate = self._join_hint_tokens([*tokens, token])
            if self._display_width(candidate) > columns:
                break
            tokens.append(token)

        text = self._join_hint_tokens(tokens)
        if text != full_text:
            ellipsis_candidate = f"{text}{_HINT_SEPARATOR}..."
            if self._display_width(ellipsis_candidate) <= columns:
                return ellipsis_candidate
        return self._truncate_with_ellipsis(text, columns)

    def _bottom_toolbar(self) -> HTML:
        columns = self._toolbar_columns()
        status = escape(self._compose_toolbar_hint(columns))
        return HTML(f"<bottom-toolbar> {status} </bottom-toolbar>")
