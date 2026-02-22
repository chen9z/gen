from __future__ import annotations

DEFAULT_MAX_LINES = 2000
DEFAULT_MAX_BYTES = 50 * 1024
GREP_MAX_LINE_LENGTH = 500


def format_size(bytes_value: int) -> str:
    if bytes_value < 1024:
        return f"{bytes_value}B"
    if bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.1f}KB"
    return f"{bytes_value / (1024 * 1024):.1f}MB"


def truncate_head(content: str, max_lines: int = DEFAULT_MAX_LINES, max_bytes: int = DEFAULT_MAX_BYTES) -> dict:
    total_bytes = len(content.encode("utf-8"))
    lines = content.split("\n")
    total_lines = len(lines)
    if total_lines <= max_lines and total_bytes <= max_bytes:
        return {
            "content": content,
            "truncated": False,
            "truncatedBy": None,
            "totalLines": total_lines,
            "totalBytes": total_bytes,
            "outputLines": total_lines,
            "outputBytes": total_bytes,
            "lastLinePartial": False,
            "firstLineExceedsLimit": False,
            "maxLines": max_lines,
            "maxBytes": max_bytes,
        }

    first_line_bytes = len(lines[0].encode("utf-8")) if lines else 0
    if first_line_bytes > max_bytes:
        return {
            "content": "",
            "truncated": True,
            "truncatedBy": "bytes",
            "totalLines": total_lines,
            "totalBytes": total_bytes,
            "outputLines": 0,
            "outputBytes": 0,
            "lastLinePartial": False,
            "firstLineExceedsLimit": True,
            "maxLines": max_lines,
            "maxBytes": max_bytes,
        }

    output_lines: list[str] = []
    output_bytes = 0
    truncated_by = "lines"

    for i, line in enumerate(lines[:max_lines]):
        add = len(line.encode("utf-8")) + (1 if i > 0 else 0)
        if output_bytes + add > max_bytes:
            truncated_by = "bytes"
            break
        output_lines.append(line)
        output_bytes += add

    output = "\n".join(output_lines)
    return {
        "content": output,
        "truncated": True,
        "truncatedBy": truncated_by,
        "totalLines": total_lines,
        "totalBytes": total_bytes,
        "outputLines": len(output_lines),
        "outputBytes": len(output.encode("utf-8")),
        "lastLinePartial": False,
        "firstLineExceedsLimit": False,
        "maxLines": max_lines,
        "maxBytes": max_bytes,
    }


def truncate_tail(content: str, max_lines: int = DEFAULT_MAX_LINES, max_bytes: int = DEFAULT_MAX_BYTES) -> dict:
    total_bytes = len(content.encode("utf-8"))
    lines = content.split("\n")
    total_lines = len(lines)
    if total_lines <= max_lines and total_bytes <= max_bytes:
        return {
            "content": content,
            "truncated": False,
            "truncatedBy": None,
            "totalLines": total_lines,
            "totalBytes": total_bytes,
            "outputLines": total_lines,
            "outputBytes": total_bytes,
            "lastLinePartial": False,
            "firstLineExceedsLimit": False,
            "maxLines": max_lines,
            "maxBytes": max_bytes,
        }

    out: list[str] = []
    bytes_count = 0
    truncated_by = "lines"
    last_line_partial = False

    for i in range(len(lines) - 1, -1, -1):
        if len(out) >= max_lines:
            truncated_by = "lines"
            break
        line = lines[i]
        add = len(line.encode("utf-8")) + (1 if out else 0)
        if bytes_count + add > max_bytes:
            truncated_by = "bytes"
            if not out:
                encoded = line.encode("utf-8")
                clipped = encoded[-max_bytes:]
                while clipped and (clipped[0] & 0xC0) == 0x80:
                    clipped = clipped[1:]
                out.insert(0, clipped.decode("utf-8", errors="ignore"))
                last_line_partial = True
            break
        out.insert(0, line)
        bytes_count += add

    output = "\n".join(out)
    return {
        "content": output,
        "truncated": True,
        "truncatedBy": truncated_by,
        "totalLines": total_lines,
        "totalBytes": total_bytes,
        "outputLines": len(out),
        "outputBytes": len(output.encode("utf-8")),
        "lastLinePartial": last_line_partial,
        "firstLineExceedsLimit": False,
        "maxLines": max_lines,
        "maxBytes": max_bytes,
    }


def truncate_line(text: str, max_chars: int = GREP_MAX_LINE_LENGTH) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[: max_chars - 12] + "...[truncated]", True
