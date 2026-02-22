from __future__ import annotations

from pathlib import Path

from gen_agent.models.content import TextContent
from gen_agent.models.tools import LsInput

from .base import Tool
from .path_utils import resolve_to_cwd
from .truncate import DEFAULT_MAX_BYTES, truncate_head


class LsTool(Tool):
    name = "ls"
    label = "ls"
    description = "List directory contents."
    input_model = LsInput

    def __init__(self, cwd: str):
        self.cwd = cwd

    def _display_name(self, path: Path) -> str:
        token = path.name
        if path.is_dir():
            token += "/"
        return token

    async def execute(self, params: LsInput) -> tuple[list[TextContent], dict | None]:
        root = resolve_to_cwd(params.path, self.cwd)
        if not root.exists():
            raise FileNotFoundError(f"Path not found: {params.path}")
        if not root.is_dir():
            raise NotADirectoryError(f"Not a directory: {params.path}")
        limit = max(1, params.limit or 500)

        lines: list[str] = []
        entries = sorted(root.iterdir(), key=lambda p: str(p).lower())
        for entry in entries:
            lines.append(self._display_name(entry))
            if len(lines) >= limit:
                break

        if not lines:
            return [TextContent(text="(empty directory)")], None

        raw = "\n".join(lines)
        truncation = truncate_head(raw, max_lines=100_000, max_bytes=DEFAULT_MAX_BYTES)
        output = truncation["content"]
        notices: list[str] = []
        details: dict[str, object] = {}
        if len(lines) >= limit:
            notices.append(f"{limit} entries limit reached. Use limit={limit * 2} for more")
            details["entryLimitReached"] = limit
        if truncation["truncated"]:
            notices.append(f"{DEFAULT_MAX_BYTES // 1024}KB limit reached")
            details["truncation"] = truncation
        if notices:
            output += f"\n\n[{' '.join(notices)}]"

        return [TextContent(text=output)], (details or None)
