from __future__ import annotations

from pathlib import Path

from gen_agent.models.settings import SettingsModel, deep_merge_dict

from .paths import ensure_dir, settings_paths


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return SettingsModel.model_validate_json(path.read_text(encoding="utf-8")).model_dump(
            by_alias=True, exclude_none=True
        )
    except Exception:
        try:
            import json

            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}


def load_settings(cwd: str | Path) -> tuple[SettingsModel, SettingsModel, SettingsModel]:
    global_path, project_path = settings_paths(cwd)
    global_raw = _load_json(global_path)
    project_raw = _load_json(project_path)
    merged = deep_merge_dict(global_raw, project_raw)
    global_settings = SettingsModel.model_validate(global_raw)
    project_settings = SettingsModel.model_validate(project_raw)
    merged_settings = SettingsModel.model_validate(merged)
    return global_settings, project_settings, merged_settings


def save_settings(cwd: str | Path, settings: SettingsModel, scope: str = "global") -> Path:
    global_path, project_path = settings_paths(cwd)
    target = global_path if scope == "global" else project_path
    ensure_dir(target.parent)
    target.write_text(settings.model_dump_json(indent=2, by_alias=True, exclude_none=True), encoding="utf-8")
    return target
