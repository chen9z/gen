from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from .events import AgentEvent, AgentSessionEvent
from .messages import AgentMessage
from .rpc import RpcCommand, RpcResponse
from .session import FileEntry, SessionEntry
from .settings import AuthModel, ModelConfigModel, SettingsModel
from .tools import BashInput, EditInput, FindInput, GrepInput, LsInput, ReadInput, ToolResult, WriteInput


SCHEMA_OBJECTS: dict[str, Any] = {
    "AgentMessage": TypeAdapter(AgentMessage),
    "AgentEvent": TypeAdapter(AgentEvent),
    "AgentSessionEvent": TypeAdapter(AgentSessionEvent),
    "FileEntry": TypeAdapter(FileEntry),
    "SessionEntry": TypeAdapter(SessionEntry),
    "SettingsModel": SettingsModel,
    "AuthModel": AuthModel,
    "ModelConfigModel": ModelConfigModel,
    "RpcCommand": TypeAdapter(RpcCommand),
    "RpcResponse": RpcResponse,
    "ReadInput": ReadInput,
    "WriteInput": WriteInput,
    "EditInput": EditInput,
    "BashInput": BashInput,
    "GrepInput": GrepInput,
    "FindInput": FindInput,
    "LsInput": LsInput,
    "ToolResult": ToolResult,
}


def export_schemas(output_dir: str | Path) -> list[Path]:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for name, obj in SCHEMA_OBJECTS.items():
        path = out_dir / f"{name}.schema.json"
        if hasattr(obj, "model_json_schema"):
            schema = obj.model_json_schema()
        else:
            schema = obj.json_schema()
        path.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")
        written.append(path)

    return written
