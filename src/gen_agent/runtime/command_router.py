from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .session_runtime import SessionRuntime


class CommandRouter:
    def __init__(self, runtime: "SessionRuntime") -> None:
        self._runtime = runtime

    async def handle(self, text: str) -> tuple[bool, str | None]:
        if not text.startswith("/"):
            return False, None

        command, _, rest = text[1:].partition(" ")
        command = command.strip()
        rest = rest.strip()

        if command == "quit":
            raise SystemExit(0)
        if command == "new":
            self._runtime.session_manager.new_session()
            return True, "Started new session"
        if command == "reload":
            diagnostics = self._runtime.reload_resources()
            lines = ["Reloaded resources"]
            for key in ("skills", "prompts", "themes", "extensions"):
                items = diagnostics.get(key) or []
                if items:
                    lines.append("")
                    lines.append(f"{key}:")
                    lines.extend(f"- {item}" for item in items[:20])
            return True, "\n".join(lines)
        if command == "model":
            if not rest:
                return True, f"Current model: {self._runtime.provider_name}/{self._runtime.model_id}"
            model_value, thinking = self._runtime._split_model_thinking(rest)
            self._runtime.provider_name, self._runtime.model_id = self._runtime._resolve_provider_and_model(
                None,
                model_value,
            )
            self._runtime.session_manager.append_model_change(
                self._runtime.provider_name,
                self._runtime.model_id,
            )
            if thinking:
                self._runtime.set_thinking_level(thinking)
            return True, f"Model set to {self._runtime.provider_name}/{self._runtime.model_id}"
        if command == "name":
            if rest:
                self._runtime.session_manager.set_session_name(rest)
                return True, f"Session name set to {rest}"
            return True, "Usage: /name <name>"
        if command == "session":
            state = self._runtime.get_state()
            return True, f"Session: {state}"
        if command == "hotkeys":
            return (
                True,
                "Ctrl+L/Ctrl+P cycle-next | Ctrl+Shift+P cycle-prev | Ctrl+N new-session | Ctrl+R resume | Ctrl+T tree | Ctrl+K compact",
            )
        if command == "settings":
            return True, self._runtime._handle_settings_command(rest)
        if command == "compact":
            return True, self._runtime._handle_manual_compact()
        if command == "tree":
            return True, self._runtime._handle_tree_command(rest)
        if command == "fork":
            return True, self._runtime._handle_fork_command(rest)
        if command == "resume":
            return True, self._runtime._handle_resume_command(rest)
        if command == "scoped-models":
            return True, self._runtime._handle_scoped_models_command(rest)

        ext_cmds = self._runtime.extension_runner.get_commands()
        if command in ext_cmds:
            result = ext_cmds[command].handler(rest, self._runtime)
            if asyncio.iscoroutine(result):
                result = await result
            if isinstance(result, str):
                return True, result
            return True, f"Executed extension command /{command}"

        return True, f"Unknown command: /{command}"
