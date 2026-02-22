from __future__ import annotations

import os
from pathlib import Path

APP_DIR_NAME = "gen-agent"
PROJECT_DIR_NAME = ".gen"


def home_dir() -> Path:
    return Path.home()


def xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", home_dir() / ".config"))


def global_root() -> Path:
    return xdg_config_home() / APP_DIR_NAME


def project_root(cwd: str | Path) -> Path:
    return Path(cwd).resolve() / PROJECT_DIR_NAME


def settings_paths(cwd: str | Path) -> tuple[Path, Path]:
    return global_root() / "settings.json", project_root(cwd) / "settings.json"


def auth_path() -> Path:
    return global_root() / "auth.json"


def models_path() -> Path:
    return global_root() / "models.json"


def sessions_root() -> Path:
    return global_root() / "sessions"


def session_dir_for_cwd(cwd: str | Path) -> Path:
    safe = str(Path(cwd).resolve()).lstrip("/").replace("/", "-").replace(":", "-")
    return sessions_root() / f"--{safe}--"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def global_resource_dir(kind: str) -> Path:
    return global_root() / kind


def project_resource_dir(cwd: str | Path, kind: str) -> Path:
    return project_root(cwd) / kind


def context_file_candidates(directory: Path) -> list[Path]:
    return [directory / "AGENTS.md", directory / "CLAUDE.md"]


def first_context_file(directory: Path) -> Path | None:
    for candidate in context_file_candidates(directory):
        if candidate.exists():
            return candidate
    return None
