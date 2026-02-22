from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from gen_agent.models.content import UserContentBlock

from .base import Tool
from .bash import BashTool
from .edit import EditTool
from .find import FindTool
from .grep import GrepTool
from .ls import LsTool
from .read import ReadTool
from .write import WriteTool


class ToolRegistry:
    def __init__(self, tools: list[Tool]):
        self.tools = {tool.name: tool for tool in tools}

    async def execute(self, name: str, args: dict[str, Any]) -> tuple[list[UserContentBlock], Any | None, bool]:
        tool = self.tools.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")

        try:
            validated = tool.input_model.model_validate(args)
        except ValidationError as exc:
            raise ValueError(f"Invalid arguments for tool {name}: {exc}") from exc

        content, details = await tool.execute(validated)
        return content, details, False


DEFAULT_TOOL_NAMES = ["read", "bash", "edit", "write"]
READONLY_TOOL_NAMES = ["read", "grep", "find", "ls"]


def create_all_tools(cwd: str, shell_command_prefix: str | None = None) -> dict[str, Tool]:
    tools: list[Tool] = [
        ReadTool(cwd),
        BashTool(cwd, command_prefix=shell_command_prefix),
        EditTool(cwd),
        WriteTool(cwd),
        GrepTool(cwd),
        FindTool(cwd),
        LsTool(cwd),
    ]
    return {tool.name: tool for tool in tools}


def create_tool_registry(
    cwd: str,
    enabled_names: list[str] | None = None,
    shell_command_prefix: str | None = None,
) -> ToolRegistry:
    all_tools = create_all_tools(cwd, shell_command_prefix=shell_command_prefix)
    names = enabled_names or DEFAULT_TOOL_NAMES
    selected = [all_tools[name] for name in names if name in all_tools]
    return ToolRegistry(selected)
