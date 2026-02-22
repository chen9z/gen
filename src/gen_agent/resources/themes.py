from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Theme:
    name: str
    data: dict
    source_path: str


def load_themes(paths: list[str]) -> tuple[list[Theme], list[str]]:
    themes: list[Theme] = []
    diagnostics: list[str] = []

    for raw in paths:
        p = Path(raw).expanduser().resolve()
        if not p.exists():
            continue
        files = [p] if p.is_file() and p.suffix == ".json" else [*p.glob("*.json")] if p.is_dir() else []

        for file in files:
            try:
                import json

                data = json.loads(file.read_text(encoding="utf-8"))
                themes.append(Theme(name=data.get("name", file.stem), data=data, source_path=str(file)))
            except Exception as exc:
                diagnostics.append(f"{file}: {exc}")

    unique: dict[str, Theme] = {}
    for theme in themes:
        if theme.name not in unique:
            unique[theme.name] = theme
        else:
            diagnostics.append(f"theme name collision: {theme.name}")

    return list(unique.values()), diagnostics
