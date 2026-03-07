"""Shared tool key argument extraction and name normalization."""

from __future__ import annotations

import os
from typing import Any

TOOL_KEY_ARGS: dict[str, list[str]] = {
    "Read": ["path", "file_path"],
    "Write": ["path", "file_path"],
    "Edit": ["path", "file_path"],
    "Bash": ["command"],
    "Grep": ["pattern", "path"],
    "Find": ["pattern", "path"],
    "Ls": ["path"],
}

# Known tool name normalizations (lowercase -> display)
_TOOL_NAME_MAP: dict[str, str] = {
    "read": "Read",
    "write": "Write",
    "edit": "Edit",
    "bash": "Bash",
    "grep": "Grep",
    "find": "Find",
    "ls": "Ls",
    "glob": "Glob",
    "webfetch": "WebFetch",
    "websearch": "WebSearch",
    "notebookedit": "NotebookEdit",
}


def normalize_tool_name(name: str) -> str:
    """Normalize tool name for display (e.g. 'read' -> 'Read')."""
    mapped = _TOOL_NAME_MAP.get(name.lower())
    if mapped:
        return mapped
    if name.islower():
        return name.capitalize()
    return name


def _shorten_path(path: str, limit: int = 40) -> str:
    """Show basename, or tail of path if longer than limit."""
    if len(path) <= limit:
        return path
    base = os.path.basename(path)
    if len(base) <= limit:
        return base
    return base[:limit - 3] + "..."


def extract_tool_key_arg(name: str, args: dict[str, Any]) -> str:
    """Extract the most relevant argument for display."""
    normalized = normalize_tool_name(name)
    keys = TOOL_KEY_ARGS.get(normalized, [])
    for key in keys:
        value = args.get(key)
        if isinstance(value, str) and value.strip():
            if key in ("path", "file_path"):
                return _shorten_path(value)
            return value[:40] + "..." if len(value) > 40 else value
    for value in args.values():
        if isinstance(value, str) and value.strip():
            return value[:40] + "..." if len(value) > 40 else value
    return ""


def extract_key_arg_from_json(name: str, args_json: str) -> str:
    """Extract key arg from a JSON args string (e.g. during streaming)."""
    import json as _json

    try:
        args = _json.loads(args_json)
    except (ValueError, TypeError):
        return ""
    if not isinstance(args, dict):
        return ""
    return extract_tool_key_arg(name, args)
