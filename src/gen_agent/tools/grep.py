from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from gen_agent.models.content import TextContent
from gen_agent.models.tools import GrepInput

from .base import Tool
from .path_utils import resolve_to_cwd
from .truncate import DEFAULT_MAX_BYTES, truncate_head, truncate_line


class GrepTool(Tool):
    name = "grep"
    label = "grep"
    description = "Search text content in files."
    input_model = GrepInput

    def __init__(self, cwd: str):
        self.cwd = cwd

    def _relative_path(self, file_path: Path, search_root: Path) -> str:
        if search_root.is_dir():
            try:
                rel = file_path.relative_to(search_root)
                return str(rel).replace(os.sep, "/")
            except Exception:
                pass
        return file_path.name

    def _scan_fallback(self, root: Path, params: GrepInput, regex: re.Pattern[str]) -> list[str]:
        files: list[Path]
        if root.is_file():
            files = [root]
        else:
            pattern = params.glob or "*"
            files = [p for p in root.rglob(pattern) if p.is_file()]

        matches: list[str] = []
        for file in files:
            try:
                lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, start=1):
                if regex.search(line):
                    clipped, _ = truncate_line(line)
                    matches.append(f"{self._relative_path(file, root)}:{i}: {clipped}")
                    if len(matches) >= params.limit:
                        return matches
        return matches

    def _scan_with_rg(self, root: Path, params: GrepInput) -> list[str] | None:
        rg_path = shutil.which("rg")
        if not rg_path:
            return None

        search_cwd = str(root if root.is_dir() else root.parent)
        search_target = "." if root.is_dir() else root.name
        args = [rg_path, "--line-number", "--color=never", "--hidden"]
        if params.ignore_case:
            args.append("--ignore-case")
        if params.literal:
            args.append("--fixed-strings")
        if params.context and params.context > 0:
            args.extend(["-C", str(params.context)])
        if params.glob:
            args.extend(["--glob", params.glob])
        args.extend([params.pattern, search_target])

        proc = subprocess.run(
            args,
            cwd=search_cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode not in {0, 1}:
            raise RuntimeError(proc.stderr.strip() or f"rg exited with code {proc.returncode}")
        output = proc.stdout.strip()
        if not output:
            return []
        lines = [self._normalize_rg_line(line) for line in output.splitlines() if line.strip()]
        return lines

    def _normalize_rg_line(self, line: str) -> str:
        if line == "--":
            return line
        match = re.match(r"^(?P<path>.+?):(?P<line>\d+):(.*)$", line)
        if match:
            path_token = match.group("path").removeprefix("./")
            line_no = match.group("line")
            text = match.group(3).lstrip()
            return f"{path_token}:{line_no}: {text}"
        context_match = re.match(r"^(?P<path>.+?)-(?P<line>\d+)-(.*)$", line)
        if context_match:
            path_token = context_match.group("path").removeprefix("./")
            line_no = context_match.group("line")
            text = context_match.group(3).lstrip()
            return f"{path_token}-{line_no}- {text}"
        return line.removeprefix("./")

    async def execute(self, params: GrepInput) -> tuple[list[TextContent], dict | None]:
        root = resolve_to_cwd(params.path, self.cwd)
        if not root.exists():
            raise FileNotFoundError(f"Path not found: {params.path}")

        if params.limit < 1:
            params.limit = 1

        if params.literal:
            regex_pattern = re.escape(params.pattern)
        else:
            regex_pattern = params.pattern
        regex_flags = re.IGNORECASE if params.ignore_case else 0
        regex = re.compile(regex_pattern, flags=regex_flags)

        matches = self._scan_with_rg(root, params)
        if matches is None:
            matches = self._scan_fallback(root, params, regex)
        if params.limit and len(matches) > params.limit:
            matches = matches[: params.limit]

        if not matches:
            return [TextContent(text="No matches found")], None

        content = "\n".join(matches)
        truncation = truncate_head(content, max_lines=10_000, max_bytes=DEFAULT_MAX_BYTES)
        output = truncation["content"]
        notices: list[str] = []
        details: dict[str, object] = {}
        if len(matches) >= params.limit:
            notices.append(f"{params.limit} matches limit reached. Use limit={params.limit * 2} for more, or refine pattern")
            details["matchLimitReached"] = params.limit
        if truncation["truncated"]:
            notices.append(f"{DEFAULT_MAX_BYTES // 1024}KB limit reached")
            details["truncation"] = truncation
        if notices:
            output += f"\n\n[{' '.join(notices)}]"
        return [TextContent(text=output)], (details or None)
