from __future__ import annotations

import os
import re
import time
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

from prompt_toolkit.completion import CompleteEvent, Completer, Completion, FuzzyCompleter, WordCompleter
from prompt_toolkit.document import Document


class SlashFuzzyCompleter(Completer):
    def __init__(self, command_provider: Callable[[], Sequence[str]]) -> None:
        super().__init__()
        self._command_provider = command_provider

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        _ = complete_event
        text = document.text_before_cursor
        if not text.startswith("/"):
            return
        if " " in text.strip():
            return
        token = text[1:].strip()
        commands = sorted(set(self._command_provider()))
        words = [command for command in commands if command]
        if not words:
            return
        base = WordCompleter(words, WORD=False, sentence=True)
        fuzzy = FuzzyCompleter(base, WORD=False)
        mention_doc = Document(text=token, cursor_position=len(token))

        seen: set[str] = set()
        for candidate in fuzzy.get_completions(mention_doc, complete_event):
            command = candidate.text
            if command in seen:
                continue
            seen.add(command)
            yield Completion(
                text=f"/{command}",
                start_position=-len(text),
                display=f"/{command}",
            )


class AtPathCompleter(Completer):
    _FRAGMENT_PATTERN = re.compile(r"[^\s@]+")
    _IGNORED_NAMES = frozenset(
        {
            ".git",
            ".venv",
            "node_modules",
            "dist",
            "build",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            ".idea",
            ".vscode",
        }
    )

    def __init__(self, root: Path, *, refresh_interval: float = 2.0, limit: int = 1500) -> None:
        self._root = root
        self._refresh_interval = refresh_interval
        self._limit = limit
        self._cache_time: float = 0.0
        self._cached_paths: list[str] = []

        self._word_completer = WordCompleter(self._get_paths, WORD=False, pattern=self._FRAGMENT_PATTERN)
        self._fuzzy = FuzzyCompleter(self._word_completer, WORD=False)

    @classmethod
    def _is_ignored(cls, name: str) -> bool:
        return not name or name in cls._IGNORED_NAMES

    def _get_paths(self) -> list[str]:
        now = time.monotonic()
        if now - self._cache_time <= self._refresh_interval:
            return self._cached_paths

        paths: list[str] = []
        try:
            for current_root, dirs, files in os.walk(self._root):
                dirs[:] = sorted(d for d in dirs if not self._is_ignored(d))
                relative_root = Path(current_root).relative_to(self._root)
                if relative_root.parts and any(self._is_ignored(part) for part in relative_root.parts):
                    dirs[:] = []
                    continue

                if relative_root.parts:
                    paths.append(relative_root.as_posix() + "/")
                    if len(paths) >= self._limit:
                        break

                for file_name in sorted(files):
                    if self._is_ignored(file_name):
                        continue
                    candidate = (relative_root / file_name).as_posix()
                    if candidate:
                        paths.append(candidate)
                    if len(paths) >= self._limit:
                        break
                if len(paths) >= self._limit:
                    break
        except OSError:
            return self._cached_paths

        self._cached_paths = paths
        self._cache_time = now
        return self._cached_paths

    @staticmethod
    def _extract_fragment(text: str) -> str | None:
        index = text.rfind("@")
        if index == -1:
            return None
        if index > 0 and text[index - 1].isalnum():
            return None
        fragment = text[index + 1 :]
        if any(ch.isspace() for ch in fragment):
            return None
        return fragment

    @staticmethod
    def _rank(fragment: str, candidate: str) -> tuple[int, str]:
        frag_lower = fragment.lower()
        base = candidate.rstrip("/").split("/")[-1].lower()
        if base.startswith(frag_lower):
            return (0, candidate)
        if frag_lower in base:
            return (1, candidate)
        return (2, candidate)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        fragment = self._extract_fragment(document.text_before_cursor)
        if fragment is None:
            return

        mention_doc = Document(text=fragment, cursor_position=len(fragment))
        candidates = list(self._fuzzy.get_completions(mention_doc, complete_event))
        dedup: dict[str, Completion] = {}
        for item in candidates:
            dedup.setdefault(item.text, item)
        ordered = sorted(dedup.keys(), key=lambda item: self._rank(fragment, item))

        for candidate in ordered:
            yield Completion(
                text=candidate,
                start_position=-len(fragment),
                display=candidate,
            )


class HybridCompleter(Completer):
    def __init__(self, slash: SlashFuzzyCompleter, at_path: AtPathCompleter) -> None:
        self._slash = slash
        self._at_path = at_path

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        text = document.text_before_cursor
        if AtPathCompleter._extract_fragment(text) is not None:
            yield from self._at_path.get_completions(document, complete_event)
            return
        yield from self._slash.get_completions(document, complete_event)
