from __future__ import annotations

import os
import subprocess

_COMMAND_RESULT_CACHE: dict[str, str | None] = {}


def resolve_config_value(config: str) -> str | None:
    if config.startswith("!"):
        return _execute_command(config)
    env_value = os.environ.get(config)
    return env_value or config


def resolve_headers(headers: dict[str, str] | None) -> dict[str, str] | None:
    if not headers:
        return None
    resolved: dict[str, str] = {}
    for key, value in headers.items():
        resolved_value = resolve_config_value(value)
        if resolved_value:
            resolved[key] = resolved_value
    return resolved or None


def clear_config_value_cache() -> None:
    _COMMAND_RESULT_CACHE.clear()


def _execute_command(command_config: str) -> str | None:
    if command_config in _COMMAND_RESULT_CACHE:
        return _COMMAND_RESULT_CACHE[command_config]

    command = command_config[1:]
    result: str | None
    try:
        completed = subprocess.run(
            command,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        output = (completed.stdout or "").strip()
        result = output or None
    except Exception:
        result = None

    _COMMAND_RESULT_CACHE[command_config] = result
    return result
