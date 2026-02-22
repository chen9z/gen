from __future__ import annotations

import base64
from pathlib import Path

from gen_agent.models.content import ImageContent, TextContent
from gen_agent.models.tools import ReadInput, TruncationResult

from .base import Tool
from .path_utils import resolve_read_path
from .truncate import DEFAULT_MAX_BYTES, format_size, truncate_head

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}
_IMAGE_MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
}


def _detect_image_mime(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in _IMAGE_EXTS:
        return _IMAGE_MIME_BY_EXT.get(ext, "application/octet-stream")

    try:
        head = path.read_bytes()[:32]
    except Exception:
        return None

    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if head.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if head.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if head.startswith(b"BM"):
        return "image/bmp"
    if len(head) >= 12 and head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    if head.startswith((b"II*\x00", b"MM\x00*")):
        return "image/tiff"
    return None


class ReadTool(Tool):
    name = "read"
    label = "read"
    description = (
        "Read file contents. Text output truncated to 2000 lines or 50KB. "
        "Use offset/limit for large files."
    )
    input_model = ReadInput

    def __init__(self, cwd: str):
        self.cwd = cwd

    async def execute(self, params: ReadInput) -> tuple[list[TextContent], TruncationResult | None]:
        path = resolve_read_path(params.path, self.cwd)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {params.path}")
        if not path.is_file():
            raise IsADirectoryError(f"Path is not a file: {params.path}")

        mime = _detect_image_mime(path)
        if mime:
            data = base64.b64encode(path.read_bytes()).decode("utf-8")
            return [
                TextContent(text=f"Read image file [{mime}]"),
                ImageContent(data=data, mimeType=mime),
            ], None

        raw = path.read_text(encoding="utf-8", errors="replace")
        lines = raw.split("\n")
        start_idx = max(0, (params.offset or 1) - 1)
        if start_idx >= len(lines):
            raise ValueError(f"Offset {params.offset} is beyond end of file ({len(lines)} lines total)")

        selected = lines[start_idx : (start_idx + params.limit) if params.limit else None]
        segment = "\n".join(selected)
        trunc = truncate_head(segment)

        output = trunc["content"]
        total_file_lines = len(lines)
        if trunc["firstLineExceedsLimit"]:
            line_size = len(lines[start_idx].encode("utf-8"))
            output = (
                f"[Line {start_idx + 1} is {format_size(line_size)}, exceeds {format_size(DEFAULT_MAX_BYTES)} limit. "
                f"Use bash: sed -n '{start_idx + 1}p' {params.path} | head -c {DEFAULT_MAX_BYTES}]"
            )
        elif trunc["truncated"]:
            end_line = start_idx + trunc["outputLines"]
            next_offset = end_line + 1
            if trunc["truncatedBy"] == "lines":
                output = f"{output}\n\n[Showing lines {start_idx + 1}-{end_line} of {total_file_lines}. Use offset={next_offset} to continue.]"
            else:
                output = f"{output}\n\n[Showing lines {start_idx + 1}-{end_line} of {total_file_lines} ({format_size(DEFAULT_MAX_BYTES)} limit). Use offset={next_offset} to continue.]"
        elif params.limit and start_idx + params.limit < total_file_lines:
            next_offset = start_idx + params.limit + 1
            remaining = total_file_lines - (start_idx + params.limit)
            output = f"{output}\n\n[{remaining} more lines in file. Use offset={next_offset} to continue.]"

        detail = TruncationResult.model_validate(trunc) if trunc["truncated"] else None
        return [TextContent(text=output)], detail
