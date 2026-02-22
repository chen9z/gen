from __future__ import annotations

import time
from typing import Annotated, Any, Literal

from pydantic import Field

from .content import AssistantContentBlock, ModelBase, Usage, UserContentBlock


def now_ms() -> int:
    return int(time.time() * 1000)


class UserMessage(ModelBase):
    role: Literal["user"] = "user"
    content: str | list[UserContentBlock]
    timestamp: int = Field(default_factory=now_ms)


class AssistantMessage(ModelBase):
    role: Literal["assistant"] = "assistant"
    content: list[AssistantContentBlock]
    api: str = "chat"
    provider: str = ""
    model: str = ""
    usage: Usage = Field(default_factory=Usage)
    stop_reason: Literal["stop", "length", "toolUse", "error", "aborted"] = Field(
        default="stop", alias="stopReason"
    )
    error_message: str | None = Field(default=None, alias="errorMessage")
    timestamp: int = Field(default_factory=now_ms)


class ToolResultMessage(ModelBase):
    role: Literal["toolResult"] = "toolResult"
    tool_call_id: str = Field(alias="toolCallId")
    tool_name: str = Field(alias="toolName")
    content: list[UserContentBlock]
    details: Any | None = None
    is_error: bool = Field(default=False, alias="isError")
    timestamp: int = Field(default_factory=now_ms)


class BashExecutionMessage(ModelBase):
    role: Literal["bashExecution"] = "bashExecution"
    command: str
    output: str
    exit_code: int | None = Field(default=None, alias="exitCode")
    cancelled: bool = False
    truncated: bool = False
    full_output_path: str | None = Field(default=None, alias="fullOutputPath")
    exclude_from_context: bool = Field(default=False, alias="excludeFromContext")
    timestamp: int = Field(default_factory=now_ms)


class CustomMessage(ModelBase):
    role: Literal["custom"] = "custom"
    custom_type: str = Field(alias="customType")
    content: str | list[UserContentBlock]
    display: bool = True
    details: Any | None = None
    timestamp: int = Field(default_factory=now_ms)


class BranchSummaryMessage(ModelBase):
    role: Literal["branchSummary"] = "branchSummary"
    summary: str
    from_id: str = Field(alias="fromId")
    timestamp: int = Field(default_factory=now_ms)


class CompactionSummaryMessage(ModelBase):
    role: Literal["compactionSummary"] = "compactionSummary"
    summary: str
    tokens_before: int = Field(alias="tokensBefore")
    timestamp: int = Field(default_factory=now_ms)


AgentMessage = Annotated[
    UserMessage
    | AssistantMessage
    | ToolResultMessage
    | BashExecutionMessage
    | CustomMessage
    | BranchSummaryMessage
    | CompactionSummaryMessage,
    Field(discriminator="role"),
]
