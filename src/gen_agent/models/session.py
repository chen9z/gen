from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from .content import ModelBase
from .messages import AgentMessage

CURRENT_SESSION_VERSION = 3


class SessionHeader(ModelBase):
    type: Literal["session"] = "session"
    version: int = CURRENT_SESSION_VERSION
    id: str
    timestamp: str
    cwd: str
    parent_session: str | None = Field(default=None, alias="parentSession")


class SessionEntryBase(ModelBase):
    type: str
    id: str
    parent_id: str | None = Field(default=None, alias="parentId")
    timestamp: str


class SessionMessageEntry(SessionEntryBase):
    type: Literal["message"] = "message"
    message: AgentMessage


class ThinkingLevelChangeEntry(SessionEntryBase):
    type: Literal["thinking_level_change"] = "thinking_level_change"
    thinking_level: str = Field(alias="thinkingLevel")


class ModelChangeEntry(SessionEntryBase):
    type: Literal["model_change"] = "model_change"
    provider: str
    model_id: str = Field(alias="modelId")


class CompactionEntry(SessionEntryBase):
    type: Literal["compaction"] = "compaction"
    summary: str
    first_kept_entry_id: str = Field(alias="firstKeptEntryId")
    tokens_before: int = Field(alias="tokensBefore")
    details: Any | None = None
    from_hook: bool | None = Field(default=None, alias="fromHook")


class BranchSummaryEntry(SessionEntryBase):
    type: Literal["branch_summary"] = "branch_summary"
    from_id: str = Field(alias="fromId")
    summary: str
    details: Any | None = None
    from_hook: bool | None = Field(default=None, alias="fromHook")


class CustomEntry(SessionEntryBase):
    type: Literal["custom"] = "custom"
    custom_type: str = Field(alias="customType")
    data: Any | None = None


class LabelEntry(SessionEntryBase):
    type: Literal["label"] = "label"
    target_id: str = Field(alias="targetId")
    label: str | None = None


class SessionInfoEntry(SessionEntryBase):
    type: Literal["session_info"] = "session_info"
    name: str | None = None


SessionEntry = Annotated[
    SessionMessageEntry
    | ThinkingLevelChangeEntry
    | ModelChangeEntry
    | CompactionEntry
    | BranchSummaryEntry
    | CustomEntry
    | LabelEntry
    | SessionInfoEntry,
    Field(discriminator="type"),
]

FileEntry = Annotated[SessionHeader | SessionEntry, Field(discriminator="type")]
