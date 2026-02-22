from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .frontmatter import parse_frontmatter


@dataclass
class Skill:
    name: str
    description: str
    file_path: str
    base_dir: str
    source: str
    disable_model_invocation: bool = False


def _load_skill_file(path: Path, source: str) -> tuple[Skill | None, list[str]]:
    diagnostics: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as exc:
        return None, [f"{path}: {exc}"]

    meta, _ = parse_frontmatter(raw)
    parent = path.parent.name
    name = meta.get("name", parent)
    desc = meta.get("description", "")
    disable = meta.get("disable-model-invocation", "false").lower() == "true"

    if not desc:
        diagnostics.append(f"{path}: description is required")
        return None, diagnostics

    if len(name) > 64:
        diagnostics.append(f"{path}: name exceeds 64 chars")
    if name != parent:
        diagnostics.append(f"{path}: name does not match parent directory")

    return (
        Skill(
            name=name,
            description=desc,
            file_path=str(path),
            base_dir=str(path.parent),
            source=source,
            disable_model_invocation=disable,
        ),
        diagnostics,
    )


def load_skills(skill_paths: list[str]) -> tuple[list[Skill], list[str]]:
    skills: list[Skill] = []
    diagnostics: list[str] = []

    for raw in skill_paths:
        root = Path(raw).expanduser().resolve()
        if not root.exists():
            continue
        if root.is_file() and root.name.endswith(".md"):
            skill, diags = _load_skill_file(root, "path")
            diagnostics.extend(diags)
            if skill:
                skills.append(skill)
            continue

        for path in root.rglob("SKILL.md"):
            skill, diags = _load_skill_file(path, "path")
            diagnostics.extend(diags)
            if skill:
                skills.append(skill)

        for path in root.glob("*.md"):
            skill, diags = _load_skill_file(path, "path")
            diagnostics.extend(diags)
            if skill:
                skills.append(skill)

    unique: dict[str, Skill] = {}
    for skill in skills:
        if skill.name not in unique:
            unique[skill.name] = skill
        else:
            diagnostics.append(f"skill name collision: {skill.name}")

    return list(unique.values()), diagnostics
