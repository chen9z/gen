from __future__ import annotations

import difflib

from gen_agent.models.content import TextContent
from gen_agent.models.tools import EditInput

from .base import Tool
from .path_utils import resolve_to_cwd


def _strip_bom(text: str) -> tuple[str, str]:
    if text.startswith("\ufeff"):
        return "\ufeff", text[1:]
    return "", text


def _detect_line_ending(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    return "\n"


def _normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _restore_line_endings(text: str, ending: str) -> str:
    if ending == "\r\n":
        return text.replace("\n", "\r\n")
    return text


def _first_changed_line(old: str, new: str) -> int:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    max_common = min(len(old_lines), len(new_lines))
    for i in range(max_common):
        if old_lines[i] != new_lines[i]:
            return i + 1
    if len(old_lines) != len(new_lines):
        return max_common + 1
    return 1


class EditTool(Tool):
    name = "edit"
    label = "edit"
    description = "Replace exact text in file. oldText must be unique and exact."
    input_model = EditInput

    def __init__(self, cwd: str):
        self.cwd = cwd

    async def execute(self, params: EditInput) -> tuple[list[TextContent], dict]:
        path = resolve_to_cwd(params.path, self.cwd)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"File not found: {params.path}")

        original_raw = path.read_bytes().decode("utf-8", errors="replace")
        bom, original = _strip_bom(original_raw)
        original_line_ending = _detect_line_ending(original)

        normalized_content = _normalize_lf(original)
        normalized_old = _normalize_lf(params.old_text)
        normalized_new = _normalize_lf(params.new_text)

        occurrences = normalized_content.count(normalized_old)
        if occurrences == 0:
            raise ValueError(
                f"Could not find the exact text in {params.path}. The old text must match exactly including all whitespace and newlines."
            )
        if occurrences > 1:
            raise ValueError(
                f"Found {occurrences} occurrences of the text in {params.path}. The text must be unique. Please provide more context to make it unique."
            )

        index = normalized_content.find(normalized_old)
        updated_normalized = (
            normalized_content[:index] + normalized_new + normalized_content[index + len(normalized_old) :]
        )
        if updated_normalized == normalized_content:
            raise ValueError(
                f"No changes made to {params.path}. The replacement produced identical content. This might indicate an issue with special characters or the text not existing as expected."
            )

        updated = bom + _restore_line_endings(updated_normalized, original_line_ending)
        updated_for_diff = updated_normalized

        path.write_text(updated, encoding="utf-8")

        diff = "\n".join(
            difflib.unified_diff(
                normalized_content.splitlines(),
                updated_for_diff.splitlines(),
                fromfile=f"a/{params.path}",
                tofile=f"b/{params.path}",
                lineterm="",
            )
        )
        first_line = _first_changed_line(normalized_content, updated_for_diff)

        return [TextContent(text=f"Successfully replaced text in {params.path}.")], {
            "diff": diff,
            "firstChangedLine": first_line,
        }
