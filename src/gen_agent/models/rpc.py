from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from .content import ImageContent, ModelBase


class PromptCommand(ModelBase):
    type: Literal["prompt"] = "prompt"
    id: str | None = None
    message: str
    images: list[ImageContent] = Field(default_factory=list)
    streaming_behavior: Literal["steer", "followUp"] | None = Field(default=None, alias="streamingBehavior")


class SteerCommand(ModelBase):
    type: Literal["steer"] = "steer"
    id: str | None = None
    message: str
    images: list[ImageContent] = Field(default_factory=list)


class FollowUpCommand(ModelBase):
    type: Literal["follow_up"] = "follow_up"
    id: str | None = None
    message: str
    images: list[ImageContent] = Field(default_factory=list)


class AbortCommand(ModelBase):
    type: Literal["abort"] = "abort"
    id: str | None = None


class GetStateCommand(ModelBase):
    type: Literal["get_state"] = "get_state"
    id: str | None = None


class GetMessagesCommand(ModelBase):
    type: Literal["get_messages"] = "get_messages"
    id: str | None = None


class SetModelCommand(ModelBase):
    type: Literal["set_model"] = "set_model"
    id: str | None = None
    provider: str
    model_id: str = Field(alias="modelId")


class NewSessionCommand(ModelBase):
    type: Literal["new_session"] = "new_session"
    id: str | None = None
    parent_session: str | None = Field(default=None, alias="parentSession")


class ContinueCommand(ModelBase):
    type: Literal["continue"] = "continue"
    id: str | None = None


class CycleModelCommand(ModelBase):
    type: Literal["cycle_model"] = "cycle_model"
    id: str | None = None


class SetThinkingLevelCommand(ModelBase):
    type: Literal["set_thinking_level"] = "set_thinking_level"
    id: str | None = None
    level: Literal["off", "minimal", "low", "medium", "high", "xhigh"]


class SetSteeringModeCommand(ModelBase):
    type: Literal["set_steering_mode"] = "set_steering_mode"
    id: str | None = None
    mode: Literal["all", "one-at-a-time"]


class SetFollowUpModeCommand(ModelBase):
    type: Literal["set_follow_up_mode"] = "set_follow_up_mode"
    id: str | None = None
    mode: Literal["all", "one-at-a-time"]


class SetSessionNameCommand(ModelBase):
    type: Literal["set_session_name"] = "set_session_name"
    id: str | None = None
    name: str


class GetTreeCommand(ModelBase):
    type: Literal["get_tree"] = "get_tree"
    id: str | None = None


class SwitchTreeCommand(ModelBase):
    type: Literal["switch_tree"] = "switch_tree"
    id: str | None = None
    leaf_id: str | None = Field(default=None, alias="leafId")


class ListSessionsCommand(ModelBase):
    type: Literal["list_sessions"] = "list_sessions"
    id: str | None = None
    limit: int = 20


class ResumeSessionCommand(ModelBase):
    type: Literal["resume_session"] = "resume_session"
    id: str | None = None
    index: int | None = None
    path: str | None = None


class ForkSessionCommand(ModelBase):
    type: Literal["fork_session"] = "fork_session"
    id: str | None = None
    leaf_id: str | None = Field(default=None, alias="leafId")


class CompactCommand(ModelBase):
    type: Literal["compact"] = "compact"
    id: str | None = None


class ReloadCommand(ModelBase):
    type: Literal["reload"] = "reload"
    id: str | None = None


class ExtensionUiResponseCommand(ModelBase):
    type: Literal["extension_ui_response"] = "extension_ui_response"
    id: str
    value: str | None = None
    confirmed: bool | None = None
    cancelled: bool | None = None


RpcCommand = Annotated[
    PromptCommand
    | SteerCommand
    | FollowUpCommand
    | AbortCommand
    | GetStateCommand
    | GetMessagesCommand
    | SetModelCommand
    | NewSessionCommand
    | ContinueCommand
    | CycleModelCommand
    | SetThinkingLevelCommand
    | SetSteeringModeCommand
    | SetFollowUpModeCommand
    | SetSessionNameCommand
    | GetTreeCommand
    | SwitchTreeCommand
    | ListSessionsCommand
    | ResumeSessionCommand
    | ForkSessionCommand
    | CompactCommand
    | ReloadCommand
    | ExtensionUiResponseCommand,
    Field(discriminator="type"),
]


class RpcResponse(ModelBase):
    type: Literal["response"] = "response"
    command: str
    success: bool
    id: str | None = None
    data: dict[str, Any] | None = None
    error: str | None = None
