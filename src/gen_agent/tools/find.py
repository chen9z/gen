from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from gen_agent.models.content import TextContent
from gen_agent.models.tools import FindInput

from .base import Tool
from .path_utils import resolve_to_cwd
from .truncate import DEFAULT_MAX_BYTES, truncate_head


class FindTool(Tool):
    name = "find"
    label = "find"
    description = "Find files by glob pattern."
    input_model = FindInput

    def __init__(self, cwd: str):
        self.cwd = cwd

    def _run_fd(self, root: Path, pattern: str, limit: int) -> list[str] | None:
        fd_path = shutil.which("fd")
        if not fd_path:
            return None
        args = [
            fd_path,
            "--glob",
            "--color=never",
            "--hidden",
            "--max-results",
            str(limit),
            pattern,
            ".",
        ]
        proc = subprocess.run(
            args,
            cwd=str(root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode not in {0, 1}:
            raise RuntimeError(proc.stderr.strip() or f"fd exited with code {proc.returncode}")
        output = proc.stdout.strip()
        return [line.strip() for line in output.splitlines() if line.strip()]

    def _scan_fallback(self, root: Path, pattern: str) -> list[str]:
        out: list[str] = []
        for p in root.rglob(pattern):
            rel = str(p.relative_to(root)).replace(os.sep, "/")
            out.append(rel)
        return out

    async def execute(self, params: FindInput) -> tuple[list[TextContent], dict | None]:
        root = resolve_to_cwd(params.path, self.cwd)
        if not root.exists():
            raise FileNotFoundError(f"Path not found: {params.path}")
        if not root.is_dir():
            raise NotADirectoryError(f"Not a directory: {params.path}")

        pattern = (params.pattern or params.glob or "*").strip() or "*"
        limit = max(1, params.limit)
        matches = self._run_fd(root, pattern, limit)
        if matches is None:
            matches = self._scan_fallback(root, pattern)
            if len(matches) > limit:
                matches = matches[:limit]

        if not matches:
            return [TextContent(text="No files found matching pattern")], None

        raw = "\n".join(matches)
        truncation = truncate_head(raw, max_lines=100_000, max_bytes=DEFAULT_MAX_BYTES)
        output = truncation["content"]
        notices: list[str] = []
        details: dict[str, object] = {}
        if len(matches) >= limit:
            notices.append(f"{limit} results limit reached. Use limit={limit * 2} for more, or refine pattern")
            details["resultLimitReached"] = limit
        if truncation["truncated"]:
            notices.append(f"{DEFAULT_MAX_BYTES // 1024}KB limit reached")
            details["truncation"] = truncation
        if notices:
            output += f"\n\n[{' '.join(notices)}]"

        return [TextContent(text=output)], (details or None)
