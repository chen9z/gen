from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from gen_agent.core.paths import (
    first_context_file,
    global_root,
    global_resource_dir,
    project_resource_dir,
)

from .prompts import PromptTemplate, expand_prompt_template, load_prompt_templates
from .skills import Skill, load_skills
from .themes import Theme, load_themes


@dataclass
class ResourceDiagnostics:
    skills: list[str]
    prompts: list[str]
    themes: list[str]


@dataclass
class ResourceState:
    skills: list[Skill]
    prompts: list[PromptTemplate]
    themes: list[Theme]
    context_files: list[tuple[str, str]]
    diagnostics: ResourceDiagnostics


def _collect_context_files(cwd: Path) -> list[tuple[str, str]]:
    files: list[tuple[str, str]] = []
    seen: set[str] = set()

    # Global context first (~/.config/gen-agent/AGENTS.md or CLAUDE.md)
    global_context = first_context_file(global_root())
    if global_context and str(global_context) not in seen:
        try:
            files.append((str(global_context), global_context.read_text(encoding="utf-8")))
            seen.add(str(global_context))
        except Exception:
            pass

    candidates = []
    current = cwd.resolve()
    for _ in range(64):
        candidates.append(current)
        if current.parent == current:
            break
        current = current.parent

    for directory in reversed(candidates):
        file = first_context_file(directory)
        if file and str(file) not in seen:
            try:
                files.append((str(file), file.read_text(encoding="utf-8")))
                seen.add(str(file))
            except Exception:
                pass

    return files


class ResourceLoader:
    def __init__(self, cwd: str):
        self.cwd = Path(cwd).resolve()
        self.state = ResourceState([], [], [], [], ResourceDiagnostics([], [], []))

    def discover_paths(self) -> tuple[list[str], list[str], list[str]]:
        skill_paths = [
            str(global_resource_dir("skills")),
            str(Path.home() / ".agents" / "skills"),
            str(project_resource_dir(self.cwd, "skills")),
        ]
        prompt_paths = [str(global_resource_dir("prompts")), str(project_resource_dir(self.cwd, "prompts"))]
        theme_paths = [str(global_resource_dir("themes")), str(project_resource_dir(self.cwd, "themes"))]
        return skill_paths, prompt_paths, theme_paths

    def reload(
        self,
        extra_skill_paths: list[str] | None = None,
        extra_prompt_paths: list[str] | None = None,
        extra_theme_paths: list[str] | None = None,
        include_discovered_skills: bool = True,
        include_discovered_prompts: bool = True,
        include_discovered_themes: bool = True,
    ) -> ResourceState:
        skill_paths, prompt_paths, theme_paths = self.discover_paths()
        if not include_discovered_skills:
            skill_paths = []
        if not include_discovered_prompts:
            prompt_paths = []
        if not include_discovered_themes:
            theme_paths = []
        skill_paths.extend(extra_skill_paths or [])
        prompt_paths.extend(extra_prompt_paths or [])
        theme_paths.extend(extra_theme_paths or [])

        skills, skill_diag = load_skills(skill_paths)
        prompts, prompt_diag = load_prompt_templates(prompt_paths)
        themes, theme_diag = load_themes(theme_paths)
        context_files = _collect_context_files(self.cwd)

        self.state = ResourceState(
            skills=skills,
            prompts=prompts,
            themes=themes,
            context_files=context_files,
            diagnostics=ResourceDiagnostics(skills=skill_diag, prompts=prompt_diag, themes=theme_diag),
        )
        return self.state

    def expand_prompt(self, text: str) -> str:
        return expand_prompt_template(text, self.state.prompts)
