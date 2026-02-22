from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

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
    offset: int | None = Field(default=None, ge=1)
    limit: int | None = Field(default=None, ge=1)


class WriteInput(ModelBase):
    path: str
    content: str


class EditInput(ModelBase):
    path: str
    old_text: str = Field(alias="oldText")
    new_text: str = Field(alias="newText")


class BashInput(ModelBase):
    command: str
    timeout: int | None = Field(default=None, ge=1)


class GrepInput(ModelBase):
    pattern: str
    path: str = "."
    glob: str | None = None
    ignore_case: bool = Field(default=False, alias="ignoreCase")
    literal: bool = False
    context: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1)


class FindInput(ModelBase):
    path: str = "."
    pattern: str | None = None
    glob: str = "*"
    limit: int = Field(default=1000, ge=1)

    @model_validator(mode="after")
    def _sync_pattern(self) -> "FindInput":
        if not self.pattern:
            self.pattern = self.glob
        self.glob = self.pattern or self.glob
        return self


class LsInput(ModelBase):
    path: str = "."
    recursive: bool = False
    limit: int = Field(default=500, ge=1)
