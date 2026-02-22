from __future__ import annotations

from typing import Any

from pydantic import Field

from .content import ModelBase, UserContentBlock


class TruncationResult(ModelBase):
    content: str
    truncated: bool
    truncated_by: str | None = Field(default=None, alias="truncatedBy")
    total_lines: int = Field(alias="totalLines")
    total_bytes: int = Field(alias="totalBytes")
    output_lines: int = Field(alias="outputLines")
    output_bytes: int = Field(alias="outputBytes")
    last_line_partial: bool = Field(default=False, alias="lastLinePartial")
    first_line_exceeds_limit: bool = Field(default=False, alias="firstLineExceedsLimit")
    max_lines: int = Field(alias="maxLines")
    max_bytes: int = Field(alias="maxBytes")


class ToolResult(ModelBase):
    content: list[UserContentBlock]
    details: Any | None = None


class ReadInput(ModelBase):
    path: str
    offset: int | None = None
    limit: int | None = None


class WriteInput(ModelBase):
    path: str
    content: str


class EditInput(ModelBase):
    path: str
    old_text: str = Field(alias="oldText")
    new_text: str = Field(alias="newText")


class BashInput(ModelBase):
    command: str
    timeout: int | None = None


class GrepInput(ModelBase):
    pattern: str
    path: str = "."
    glob: str | None = None
    ignore_case: bool = Field(default=False, alias="ignoreCase")
    literal: bool = False
    context: int | None = None
    limit: int | None = None


class FindInput(ModelBase):
    path: str = "."
    pattern: str
    limit: int | None = None


class LsInput(ModelBase):
    path: str = "."
    limit: int | None = None
