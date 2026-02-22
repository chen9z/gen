from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

from gen_agent.tools.base import Tool

EventHandler = Callable[[dict[str, Any], Any], Any]


@dataclass
class ExtensionCommand:
    name: str
    description: str | None
    handler: Callable[[str, Any], Any]


@dataclass
class ExtensionFlag:
    name: str
    flag_type: str
    description: str | None = None


@dataclass
class ExtensionState:
    path: str
    tools: dict[str, Tool] = field(default_factory=dict)
    commands: dict[str, ExtensionCommand] = field(default_factory=dict)
    flags: dict[str, ExtensionFlag] = field(default_factory=dict)
    handlers: dict[str, list[EventHandler]] = field(default_factory=lambda: defaultdict(list))


class ExtensionAPI:
    def __init__(self, state: ExtensionState):
        self.state = state

    def register_tool(self, tool: Tool) -> None:
        self.state.tools[tool.name] = tool

    def register_command(self, name: str, handler: Callable[[str, Any], Any], description: str | None = None) -> None:
        self.state.commands[name] = ExtensionCommand(name=name, description=description, handler=handler)

    def register_flag(self, name: str, flag_type: str = "boolean", description: str | None = None) -> None:
        self.state.flags[name] = ExtensionFlag(name=name, flag_type=flag_type, description=description)

    def on(self, event_name: str, handler: EventHandler) -> None:
        self.state.handlers[event_name].append(handler)
