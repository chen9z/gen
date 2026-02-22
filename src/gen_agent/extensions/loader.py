from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

from .api import ExtensionAPI, ExtensionState


def _load_module_from_path(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"gen_extension_{abs(hash(path))}", path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load extension from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_extension(path: str) -> tuple[ExtensionState | None, str | None]:
    extension_path = Path(path).expanduser().resolve()
    try:
        module = _load_module_from_path(extension_path)
        register = getattr(module, "register", None) or getattr(module, "default", None)
        if not callable(register):
            return None, f"{path}: missing callable register(pi)"

        state = ExtensionState(path=str(extension_path))
        api = ExtensionAPI(state)
        register(api)
        return state, None
    except Exception as exc:
        return None, f"{path}: {exc}"


def discover_extension_files(paths: list[str]) -> list[str]:
    files: list[str] = []
    for raw in paths:
        p = Path(raw).expanduser().resolve()
        if not p.exists():
            continue
        if p.is_file() and p.suffix == ".py":
            files.append(str(p))
        elif p.is_dir():
            for file in p.rglob("*.py"):
                files.append(str(file))
    return files


class ExtensionRunner:
    def __init__(self):
        self.extensions: list[ExtensionState] = []
        self.errors: list[str] = []

    def load(self, paths: list[str]) -> None:
        self.extensions = []
        self.errors = []
        for file in discover_extension_files(paths):
            ext, error = load_extension(file)
            if error:
                self.errors.append(error)
            elif ext:
                self.extensions.append(ext)

    def emit(self, event_name: str, payload: dict[str, Any], ctx: Any) -> None:
        for ext in self.extensions:
            for handler in ext.handlers.get(event_name, []):
                handler(payload, ctx)

    def get_tools(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for ext in self.extensions:
            out.update(ext.tools)
        return out

    def get_commands(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for ext in self.extensions:
            out.update(ext.commands)
        return out

    def get_flags(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for ext in self.extensions:
            out.update(ext.flags)
        return out
