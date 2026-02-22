from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from .content import ModelBase
from .messages import AgentMessage, ToolResultMessage


class AgentStart(ModelBase):
    type: Literal["agent_start"] = "agent_start"


class AgentEnd(ModelBase):
    type: Literal["agent_end"] = "agent_end"
    messages: list[AgentMessage]


class TurnStart(ModelBase):
    type: Literal["turn_start"] = "turn_start"


class TurnEnd(ModelBase):
    type: Literal["turn_end"] = "turn_end"
    message: AgentMessage
    tool_results: list[ToolResultMessage] = Field(default_factory=list, alias="toolResults")


class MessageStart(ModelBase):
    type: Literal["message_start"] = "message_start"
    message: AgentMessage


class AssistantMessageEvent(ModelBase):
    type: Literal[
        "start",
        "text_start",
        "text_delta",
        "text_end",
        "thinking_start",
        "thinking_delta",
        "thinking_end",
        "toolcall_start",
        "toolcall_delta",
        "toolcall_end",
        "done",
        "error",
    ]
    delta: str | None = None
    content_index: int | None = Field(default=None, alias="contentIndex")
    error: str | None = None


class MessageUpdate(ModelBase):
    type: Literal["message_update"] = "message_update"
    message: AgentMessage
    assistant_message_event: AssistantMessageEvent = Field(alias="assistantMessageEvent")


class MessageEnd(ModelBase):
    type: Literal["message_end"] = "message_end"
    message: AgentMessage


class ToolExecutionStart(ModelBase):
    type: Literal["tool_execution_start"] = "tool_execution_start"
    tool_call_id: str = Field(alias="toolCallId")
    tool_name: str = Field(alias="toolName")
    args: dict[str, Any]


class ToolExecutionUpdate(ModelBase):
    type: Literal["tool_execution_update"] = "tool_execution_update"
    tool_call_id: str = Field(alias="toolCallId")
    tool_name: str = Field(alias="toolName")
    args: dict[str, Any]
    partial_result: Any = Field(alias="partialResult")


class ToolExecutionEnd(ModelBase):
    type: Literal["tool_execution_end"] = "tool_execution_end"
    tool_call_id: str = Field(alias="toolCallId")
    tool_name: str = Field(alias="toolName")
    result: Any
    is_error: bool = Field(alias="isError")


AgentEvent = Annotated[
    AgentStart
    | AgentEnd
    | TurnStart
    | TurnEnd
    | MessageStart
    | MessageUpdate
    | MessageEnd
    | ToolExecutionStart
    | ToolExecutionUpdate
    | ToolExecutionEnd,
    Field(discriminator="type"),
]


class AutoCompactionStart(ModelBase):
    type: Literal["auto_compaction_start"] = "auto_compaction_start"
    reason: Literal["threshold", "overflow"]


class AutoCompactionEnd(ModelBase):
    type: Literal["auto_compaction_end"] = "auto_compaction_end"
    result: dict[str, Any] | None = None
    aborted: bool = False
    will_retry: bool = Field(default=False, alias="willRetry")
    error_message: str | None = Field(default=None, alias="errorMessage")


class AutoRetryStart(ModelBase):
    type: Literal["auto_retry_start"] = "auto_retry_start"
    attempt: int
    max_attempts: int = Field(alias="maxAttempts")
    delay_ms: int = Field(alias="delayMs")
    error_message: str = Field(alias="errorMessage")


class AutoRetryEnd(ModelBase):
    type: Literal["auto_retry_end"] = "auto_retry_end"
    success: bool
    attempt: int
    final_error: str | None = Field(default=None, alias="finalError")


AgentSessionEvent = Annotated[
    AgentEvent | AutoCompactionStart | AutoCompactionEnd | AutoRetryStart | AutoRetryEnd,
    Field(discriminator="type"),
]
