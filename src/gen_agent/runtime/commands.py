from __future__ import annotations

import asyncio
import json
import shlex
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from gen_agent.core.settings_store import load_settings, save_settings


@dataclass
class CommandResult:
    message: str
    persist: bool = True


CommandHandler = Callable[[str], CommandResult | Awaitable[CommandResult]]


class SettingsCommandHandler:
    def __init__(
        self,
        *,
        cwd: str,
        global_settings_getter: Callable[[], Any],
        project_settings_getter: Callable[[], Any],
        settings_getter: Callable[[], Any],
        on_updated: Callable[[Any, Any, Any], None],
    ) -> None:
        self._cwd = cwd
        self._global_settings_getter = global_settings_getter
        self._project_settings_getter = project_settings_getter
        self._settings_getter = settings_getter
        self._on_updated = on_updated

    def handle(self, rest: str) -> str:
        settings = self._settings_getter()
        if not rest:
            return settings.model_dump_json(indent=2, by_alias=True)
        try:
            tokens = shlex.split(rest)
        except ValueError as exc:
            return f"Invalid /settings syntax: {exc}"
        if not tokens:
            return settings.model_dump_json(indent=2, by_alias=True)

        op = tokens[0]
        if op == "get":
            if len(tokens) < 2:
                return "Usage: /settings get <key>"
            key = tokens[1]
            data = settings.model_dump(by_alias=True, exclude_none=False)
            value = self._dict_get_nested(data, key)
            return f"{key} = {value!r}"
        if op == "set":
            if len(tokens) < 3:
                return "Usage: /settings set <key> <value> [global|project]"
            key = tokens[1]
            value = self._parse_setting_value(tokens[2])
            scope = tokens[3] if len(tokens) > 3 else "project"
            scope = "project" if scope.lower() == "project" else "global"
            target = self._global_settings_getter() if scope == "global" else self._project_settings_getter()
            dumped = target.model_dump(by_alias=True, exclude_none=False)
            self._dict_set_nested(dumped, key, value)
            validated = target.model_validate(dumped)
            save_settings(self._cwd, validated, scope=scope)
            global_settings, project_settings, merged_settings = load_settings(self._cwd)
            self._on_updated(global_settings, project_settings, merged_settings)
            return f"Updated {scope} setting: {key}={value!r}"
        return "Usage: /settings [get|set]"

    def _parse_setting_value(self, raw: str) -> Any:
        lowered = raw.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        if lowered in {"null", "none"}:
            return None
        try:
            if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
                return int(raw)
            return float(raw)
        except ValueError:
            pass
        try:
            return json.loads(raw)
        except Exception:
            return raw

    def _dict_get_nested(self, data: dict[str, Any], path: str) -> Any:
        cur: Any = data
        for key in path.split("."):
            if not isinstance(cur, dict):
                return None
            if key in cur:
                cur = cur[key]
                continue
            if key not in {item.replace("-", "_") for item in cur}:
                return None
            mapped = next(item for item in cur if item.replace("-", "_") == key)
            cur = cur[mapped]
        return cur

    def _dict_set_nested(self, data: dict[str, Any], path: str, value: Any) -> None:
        parts = path.split(".")
        cur = data
        for key in parts[:-1]:
            if key not in cur or not isinstance(cur[key], dict):
                cur[key] = {}
            cur = cur[key]
        cur[parts[-1]] = value


class CommandRegistry:
    def __init__(
        self,
        *,
        extension_commands_getter: Callable[[], dict[str, Any]],
        extension_command_context_getter: Callable[[], Any],
    ) -> None:
        self._handlers: dict[str, CommandHandler] = {}
        self._extension_commands_getter = extension_commands_getter
        self._extension_command_context_getter = extension_command_context_getter

    def register(self, name: str, handler: CommandHandler) -> None:
        self._handlers[name] = handler

    async def dispatch(self, text: str) -> CommandResult | None:
        if not text.startswith("/"):
            return None

        command, _, rest = text[1:].partition(" ")
        command = command.strip()
        rest = rest.strip()

        handler = self._handlers.get(command)
        if handler is not None:
            result = handler(rest)
            if asyncio.iscoroutine(result):
                return await result
            return result

        extension_commands = self._extension_commands_getter()
        if command in extension_commands:
            result = extension_commands[command].handler(rest, self._extension_command_context_getter())
            if asyncio.iscoroutine(result):
                result = await result
            if isinstance(result, str):
                return CommandResult(result)
            return CommandResult(f"Executed extension command /{command}")

        return CommandResult(f"Unknown command: /{command}")


def build_command_registry(
    *,
    cwd: str,
    global_settings_getter: Callable[[], Any],
    project_settings_getter: Callable[[], Any],
    settings_getter: Callable[[], Any],
    on_settings_updated: Callable[[Any, Any, Any], None],
    extension_commands_getter: Callable[[], dict[str, Any]],
    runtime_context_getter: Callable[[], Any],
    session_ops,
    model_controller,
    compaction_service,
    reload_resources: Callable[[], dict[str, list[str]]],
) -> CommandRegistry:
    registry = CommandRegistry(
        extension_commands_getter=extension_commands_getter,
        extension_command_context_getter=runtime_context_getter,
    )
    settings_handler = SettingsCommandHandler(
        cwd=cwd,
        global_settings_getter=global_settings_getter,
        project_settings_getter=project_settings_getter,
        settings_getter=settings_getter,
        on_updated=on_settings_updated,
    )

    def _cmd_quit(_rest: str) -> CommandResult:
        raise SystemExit(0)

    def _cmd_new(_rest: str) -> CommandResult:
        session_ops.new_session()
        return CommandResult("Started new session")

    def _cmd_reload(_rest: str) -> CommandResult:
        diagnostics = reload_resources()
        lines = ["Reloaded resources"]
        for key in ("skills", "prompts", "themes", "extensions"):
            items = diagnostics.get(key) or []
            if items:
                lines.extend(["", f"{key}:"])
                lines.extend(f"- {item}" for item in items[:20])
        return CommandResult("\n".join(lines))

    def _cmd_model(rest: str) -> CommandResult:
        return CommandResult(model_controller.set_model_from_text(rest))

    def _cmd_name(rest: str) -> CommandResult:
        if not rest:
            return CommandResult("Usage: /name <name>")
        session_ops.set_session_name(rest)
        return CommandResult(f"Session name set to {rest}")

    def _cmd_session(_rest: str) -> CommandResult:
        return CommandResult(f"Session: {runtime_context_getter().get_state()}")

    def _cmd_hotkeys(_rest: str) -> CommandResult:
        return CommandResult(
            "Ctrl+L/Ctrl+P cycle-next | Ctrl+Shift+P cycle-prev | Ctrl+N new-session | Ctrl+R resume | Ctrl+T tree | Ctrl+K compact"
        )

    def _cmd_settings(rest: str) -> CommandResult:
        return CommandResult(settings_handler.handle(rest))

    def _cmd_compact(_rest: str) -> CommandResult:
        return CommandResult(compaction_service.compact_now())

    def _cmd_tree(rest: str) -> CommandResult:
        tree = session_ops.get_tree(limit=50)
        entries = tree["entries"]
        if rest:
            target = rest.strip()
            if target in {"root", "none"}:
                session_ops.switch_tree(None)
                return CommandResult("Moved to root (empty context).")
            if target.isdigit():
                index = int(target) - 1
                if 0 <= index < len(entries):
                    entry = entries[index]
                    session_ops.switch_tree(entry["id"])
                    return CommandResult(f'Moved tree leaf to #{index + 1} ({entry["id"]}).')
                return CommandResult(f"Invalid tree index: {target}")
            if not session_ops.switch_tree(target):
                return CommandResult(f"Unknown entry id: {target}")
            return CommandResult(f"Moved tree leaf to {target}.")

        lines = []
        leaf = tree["leafId"]
        for idx, entry in enumerate(entries, start=1):
            mark = "*" if entry["id"] == leaf else " "
            lines.append(f'{mark} #{idx:02d} {entry["id"]} {entry["type"]} parent={entry["parentId"]}')
        if not lines:
            return CommandResult("(empty tree)")
        return CommandResult("Tree entries (use /tree <index|entry_id|root>):\n" + "\n".join(lines))

    def _cmd_fork(rest: str) -> CommandResult:
        leaf = rest.strip() or None
        new_file = session_ops.fork_session(leaf_id=leaf)
        if leaf is not None and new_file is None:
            return CommandResult(f"Unknown entry id: {leaf}")
        return CommandResult(f"Forked session to {new_file}")

    def _cmd_resume(rest: str) -> CommandResult:
        arg = rest.strip()
        if not arg:
            sessions = session_ops.list_sessions(limit=20)
            if not sessions:
                return CommandResult("No previous sessions found.")
            current_file = runtime_context_getter().session_file
            lines = []
            for idx, summary in enumerate(sessions, start=1):
                title = summary["name"] or summary["firstMessage"] or "(no title)"
                mark = "*" if current_file and summary["path"] == current_file else " "
                lines.append(f'{mark} {idx}. {summary["path"]} | messages={summary["messageCount"]} | {title}')
            return CommandResult("Recent sessions:\n" + "\n".join(lines))

        try:
            target = int(arg) if arg.isdigit() else arg
            path = session_ops.resume_session(target)
        except ValueError:
            return CommandResult("Invalid /resume target. Use /resume to list or /resume <index|path>.")
        return CommandResult(f"Resumed session: {path}")

    def _cmd_scoped_models(rest: str) -> CommandResult:
        arg = rest.strip()
        if not arg:
            patterns = model_controller.scoped_model_patterns
            if not patterns:
                return CommandResult("Scoped models disabled. Using all known models.")
            return CommandResult("Scoped patterns: " + ", ".join(patterns))
        if arg in {"clear", "off"}:
            model_controller.set_scoped_models([])
            return CommandResult("Scoped models cleared.")
        resolved = model_controller.set_scoped_models([part.strip() for part in arg.split(",") if part.strip()])
        warnings = model_controller.last_scope_warnings
        if not resolved:
            if warnings:
                return CommandResult("\n".join(["Scoped models updated: (no matches)", *warnings]))
            return CommandResult("Scoped models updated: (no matches)")
        lines = ["Scoped models updated:", *resolved]
        if warnings:
            lines.extend(["", *warnings])
        return CommandResult("\n".join(lines))

    registry.register("quit", _cmd_quit)
    registry.register("new", _cmd_new)
    registry.register("reload", _cmd_reload)
    registry.register("model", _cmd_model)
    registry.register("name", _cmd_name)
    registry.register("session", _cmd_session)
    registry.register("hotkeys", _cmd_hotkeys)
    registry.register("settings", _cmd_settings)
    registry.register("compact", _cmd_compact)
    registry.register("tree", _cmd_tree)
    registry.register("fork", _cmd_fork)
    registry.register("resume", _cmd_resume)
    registry.register("scoped-models", _cmd_scoped_models)
    return registry
