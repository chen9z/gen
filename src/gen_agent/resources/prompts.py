from __future__ import annotations

import shlex
from dataclasses import dataclass
from pathlib import Path

from .frontmatter import parse_frontmatter


@dataclass
class PromptTemplate:
    name: str
    description: str
    content: str
    source: str
    file_path: str


def parse_command_args(args_string: str) -> list[str]:
    try:
        return shlex.split(args_string)
    except ValueError:
        return [part for part in args_string.split() if part]


def substitute_args(content: str, args: list[str]) -> str:
    out = content
    for i, value in enumerate(args, start=1):
        out = out.replace(f"${i}", value)
    all_args = " ".join(args)
    out = out.replace("$@", all_args)
    out = out.replace("$ARGUMENTS", all_args)
    return out


def load_prompt_templates(paths: list[str]) -> tuple[list[PromptTemplate], list[str]]:
    templates: list[PromptTemplate] = []
    diagnostics: list[str] = []
    for raw in paths:
        p = Path(raw).expanduser().resolve()
        if not p.exists():
            continue
        files: list[Path]
        if p.is_file() and p.suffix == ".md":
            files = [p]
        elif p.is_dir():
            files = [*p.glob("*.md")]
        else:
            files = []

        for file in files:
            try:
                raw_content = file.read_text(encoding="utf-8")
            except Exception as exc:
                diagnostics.append(f"{file}: {exc}")
                continue
            meta, body = parse_frontmatter(raw_content)
            desc = meta.get("description", body.strip().splitlines()[0] if body.strip() else "")
            templates.append(
                PromptTemplate(
                    name=file.stem,
                    description=desc,
                    content=body,
                    source="path",
                    file_path=str(file),
                )
            )

    unique: dict[str, PromptTemplate] = {}
    for template in templates:
        if template.name not in unique:
            unique[template.name] = template
        else:
            diagnostics.append(f"prompt name collision: {template.name}")
    return list(unique.values()), diagnostics


def expand_prompt_template(text: str, templates: list[PromptTemplate]) -> str:
    if not text.startswith("/"):
        return text
    command, _, args = text[1:].partition(" ")
    template = next((tpl for tpl in templates if tpl.name == command), None)
    if not template:
        return text
    return substitute_args(template.content, parse_command_args(args))
