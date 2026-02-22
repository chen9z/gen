from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ModelBase(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class TextContent(ModelBase):
    type: Literal["text"] = "text"
    text: str


class ImageContent(ModelBase):
    type: Literal["image"] = "image"
    data: str
    mime_type: str = Field(alias="mimeType")


class ThinkingContent(ModelBase):
    type: Literal["thinking"] = "thinking"
    thinking: str


class ToolCallContent(ModelBase):
    type: Literal["toolCall"] = "toolCall"
    id: str
    name: str
    arguments: dict[str, Any]


UserContentBlock = Annotated[TextContent | ImageContent, Field(discriminator="type")]
AssistantContentBlock = Annotated[
    TextContent | ThinkingContent | ToolCallContent,
    Field(discriminator="type"),
]


class UsageCost(ModelBase):
    input: float = 0.0
    output: float = 0.0
    cache_read: float = Field(default=0.0, alias="cacheRead")
    cache_write: float = Field(default=0.0, alias="cacheWrite")
    total: float = 0.0


class Usage(ModelBase):
    input: int = 0
    output: int = 0
    cache_read: int = Field(default=0, alias="cacheRead")
    cache_write: int = Field(default=0, alias="cacheWrite")
    total_tokens: int = Field(default=0, alias="totalTokens")
    cost: UsageCost = Field(default_factory=UsageCost)
