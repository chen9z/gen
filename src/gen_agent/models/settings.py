from __future__ import annotations

from typing import Any, Literal

from pydantic import ConfigDict, Field, model_validator

from .content import ModelBase


class CompactionSettings(ModelBase):
    enabled: bool = True
    reserve_tokens: int = Field(default=16384, alias="reserveTokens")
    keep_recent_tokens: int = Field(default=20000, alias="keepRecentTokens")


class RetrySettings(ModelBase):
    enabled: bool = True
    max_retries: int = Field(default=3, alias="maxRetries")
    base_delay_ms: int = Field(default=2000, alias="baseDelayMs")
    max_delay_ms: int = Field(default=60000, alias="maxDelayMs")


class TerminalSettings(ModelBase):
    show_images: bool = Field(default=True, alias="showImages")
    clear_on_shrink: bool = Field(default=False, alias="clearOnShrink")


class ImageSettings(ModelBase):
    auto_resize: bool = Field(default=True, alias="autoResize")
    block_images: bool = Field(default=False, alias="blockImages")


class MarkdownSettings(ModelBase):
    code_block_indent: str = Field(default="  ", alias="codeBlockIndent")


class SettingsModel(ModelBase):
    default_provider: str | None = Field(default=None, alias="defaultProvider")
    default_model: str | None = Field(default=None, alias="defaultModel")
    default_thinking_level: Literal["off", "minimal", "low", "medium", "high", "xhigh"] | None = Field(
        default=None, alias="defaultThinkingLevel"
    )
    steering_mode: Literal["all", "one-at-a-time"] = Field(default="one-at-a-time", alias="steeringMode")
    follow_up_mode: Literal["all", "one-at-a-time"] = Field(default="one-at-a-time", alias="followUpMode")
    transport: Literal["sse", "websocket", "auto"] = "sse"
    theme: str | None = None
    quiet_startup: bool = Field(default=False, alias="quietStartup")
    enable_skill_commands: bool = Field(default=True, alias="enableSkillCommands")
    shell_path: str | None = Field(default=None, alias="shellPath")
    shell_command_prefix: str | None = Field(default=None, alias="shellCommandPrefix")
    packages: list[Any] = Field(default_factory=list)
    extensions: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    prompts: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    enabled_models: list[str] = Field(default_factory=list, alias="enabledModels")
    compaction: CompactionSettings = Field(default_factory=CompactionSettings)
    retry: RetrySettings = Field(default_factory=RetrySettings)
    terminal: TerminalSettings = Field(default_factory=TerminalSettings)
    images: ImageSettings = Field(default_factory=ImageSettings)
    markdown: MarkdownSettings = Field(default_factory=MarkdownSettings)


class ApiKeyCredential(ModelBase):
    type: Literal["api_key"] = "api_key"
    key: str


class OAuthCredential(ModelBase):
    type: Literal["oauth"] = "oauth"
    access_token: str = Field(alias="accessToken")
    refresh_token: str | None = Field(default=None, alias="refreshToken")
    expires_at: int | None = Field(default=None, alias="expiresAt")


AuthCredential = ApiKeyCredential | OAuthCredential


class AuthModel(ModelBase):
    providers: dict[str, AuthCredential] = Field(default_factory=dict)


class ProviderModelDefinition(ModelBase):
    id: str
    name: str | None = None
    api: str | None = None
    reasoning: bool | None = None
    input: list[Literal["text", "image"]] | None = None
    context_window: int | None = Field(default=None, alias="contextWindow")
    max_tokens: int | None = Field(default=None, alias="maxTokens")
    input_cost_per_million: float | None = Field(default=None, alias="inputCostPerMillion")
    output_cost_per_million: float | None = Field(default=None, alias="outputCostPerMillion")
    cache_read_cost_per_million: float | None = Field(default=None, alias="cacheReadCostPerMillion")
    cache_write_cost_per_million: float | None = Field(default=None, alias="cacheWriteCostPerMillion")
    headers: dict[str, str] | None = None

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _lift_pricing(cls, raw: Any) -> Any:
        if not isinstance(raw, dict):
            return raw
        data = dict(raw)
        pricing = data.get("pricing") if isinstance(data.get("pricing"), dict) else {}

        def _pick(*keys: str) -> Any | None:
            for key in keys:
                if key in data and data[key] is not None:
                    return data[key]
                if key in pricing and pricing[key] is not None:
                    return pricing[key]
            return None

        if data.get("inputCostPerMillion") is None:
            value = _pick(
                "inputCostPerMillion",
                "inputCostPerM",
                "inputCostPer1M",
                "promptCostPerMillion",
                "promptCostPerM",
            )
            if value is not None:
                data["inputCostPerMillion"] = value

        if data.get("outputCostPerMillion") is None:
            value = _pick(
                "outputCostPerMillion",
                "outputCostPerM",
                "outputCostPer1M",
                "completionCostPerMillion",
                "completionCostPerM",
            )
            if value is not None:
                data["outputCostPerMillion"] = value

        if data.get("cacheReadCostPerMillion") is None:
            value = _pick(
                "cacheReadCostPerMillion",
                "cacheReadCostPerM",
                "cacheReadCostPer1M",
            )
            if value is not None:
                data["cacheReadCostPerMillion"] = value

        if data.get("cacheWriteCostPerMillion") is None:
            value = _pick(
                "cacheWriteCostPerMillion",
                "cacheWriteCostPerM",
                "cacheWriteCostPer1M",
                "cacheCreationCostPerMillion",
                "cacheCreationCostPerM",
            )
            if value is not None:
                data["cacheWriteCostPerMillion"] = value

        return data


class ProviderConfigModel(ModelBase):
    base_url: str | None = Field(default=None, alias="baseUrl")
    api_key: str | None = Field(default=None, alias="apiKey")
    api: str | None = None
    headers: dict[str, str] | None = None
    models: list[ProviderModelDefinition] = Field(default_factory=list)
    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class ModelConfigModel(ModelBase):
    providers: dict[str, ProviderConfigModel] = Field(default_factory=dict)
    model_config = ConfigDict(extra="ignore", populate_by_name=True)


def deep_merge_dict(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, override in overrides.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(override, dict):
            merged[key] = deep_merge_dict(current, override)
        else:
            merged[key] = override
    return merged
