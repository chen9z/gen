from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from rich.console import RenderableType
from rich.syntax import Syntax
from rich.text import Text


@dataclass
class CodeBlock:
    """Represents a detected code block in markdown."""

    language: str
    content: str
    start_pos: int
    end_pos: int | None = None


class StreamingSyntaxHighlighter:
    """Incremental syntax highlighter for streaming markdown content.

    Detects code blocks (```language) and applies syntax highlighting
    during streaming, before the full content is available.
    """

    def __init__(self) -> None:
        self._state: Literal["text", "code_fence_start", "in_code"] = "text"
        self._current_block: CodeBlock | None = None
        self._blocks: list[CodeBlock] = []
        self._buffer = ""
        self._fence_pattern = re.compile(r"^```(\w+)?$", re.MULTILINE)

    def append(self, delta: str) -> None:
        """Append streaming text delta and update code block detection."""
        self._buffer += delta
        self._detect_blocks()

    def _detect_blocks(self) -> None:
        """Detect code block boundaries in the buffer."""
        pos = 0
        while pos < len(self._buffer):
            if self._state == "text":
                # Look for code fence start
                match = self._fence_pattern.search(self._buffer, pos)
                if match:
                    language = match.group(1) or "text"
                    self._current_block = CodeBlock(
                        language=language,
                        content="",
                        start_pos=match.end(),
                    )
                    self._state = "in_code"
                    pos = match.end()
                else:
                    break

            elif self._state == "in_code":
                # Look for code fence end
                match = self._fence_pattern.search(self._buffer, pos)
                if match and self._current_block:
                    # Found closing fence
                    self._current_block.content = self._buffer[
                        self._current_block.start_pos : match.start()
                    ].rstrip("\n")
                    self._current_block.end_pos = match.start()
                    self._blocks.append(self._current_block)
                    self._current_block = None
                    self._state = "text"
                    pos = match.end()
                else:
                    # Still in code block, update content
                    if self._current_block:
                        self._current_block.content = self._buffer[
                            self._current_block.start_pos :
                        ].rstrip("\n")
                    break

    def render_highlighted(self) -> list[RenderableType]:
        """Render the buffer with syntax highlighting for code blocks."""
        parts: list[RenderableType] = []
        last_pos = 0

        for block in self._blocks:
            # Add text before code block
            if block.start_pos > last_pos:
                text_before = self._buffer[last_pos : block.start_pos - len(block.language) - 4]
                if text_before.strip():
                    parts.append(Text(text_before))

            # Add highlighted code block
            if block.content:
                try:
                    syntax = Syntax(
                        block.content,
                        block.language,
                        theme="monokai",
                        line_numbers=False,
                        word_wrap=True,
                    )
                    parts.append(syntax)
                except Exception:
                    # Fallback to plain text if highlighting fails
                    parts.append(Text(f"```{block.language}\n{block.content}\n```"))

            last_pos = block.end_pos + 3 if block.end_pos else len(self._buffer)

        # Add remaining text after last code block
        if self._current_block:
            # Currently in an open code block
            text_before = self._buffer[last_pos : self._current_block.start_pos - len(self._current_block.language) - 4]
            if text_before.strip():
                parts.append(Text(text_before))

            # Render incomplete code block with syntax highlighting
            if self._current_block.content:
                try:
                    syntax = Syntax(
                        self._current_block.content,
                        self._current_block.language,
                        theme="monokai",
                        line_numbers=False,
                        word_wrap=True,
                    )
                    parts.append(syntax)
                except Exception:
                    parts.append(Text(f"```{self._current_block.language}\n{self._current_block.content}"))
        elif last_pos < len(self._buffer):
            # Add remaining text
            remaining = self._buffer[last_pos:]
            if remaining.strip():
                parts.append(Text(remaining))

        return parts

    def has_code_blocks(self) -> bool:
        """Check if any code blocks have been detected."""
        return bool(self._blocks or self._current_block)
