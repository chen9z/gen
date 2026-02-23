from __future__ import annotations

from datetime import datetime
from pathlib import Path

from gen_agent.resources.skills import Skill, format_skills_for_prompt

TOOL_DESCRIPTIONS: dict[str, str] = {
    "read": "Read file contents",
    "bash": "Execute bash commands (ls, grep, find, etc.)",
    "edit": "Make surgical edits to files (find exact text and replace)",
    "write": "Create or overwrite files",
    "grep": "Search file contents for patterns (respects .gitignore)",
    "find": "Find files by glob pattern (respects .gitignore)",
    "ls": "List directory contents",
}


def _find_repo_root(cwd: str) -> Path:
    current = Path(cwd).resolve()
    for directory in [current, *current.parents]:
        if (directory / "pyproject.toml").exists():
            return directory
    return current


def _format_project_context(context_files: list[tuple[str, str]]) -> str:
    if not context_files:
        return ""

    lines = ["", "", "# Project Context", "", "Project-specific instructions and guidelines:", ""]
    for file_path, content in context_files:
        lines.append(f"## {file_path}")
        lines.append("")
        lines.append(content)
        lines.append("")
    return "\n".join(lines).rstrip()


def build_system_prompt(
    *,
    cwd: str,
    custom_prompt: str | None,
    selected_tools: list[str] | None,
    append_system_prompt: str | None,
    context_files: list[tuple[str, str]],
    skills: list[Skill],
) -> str:
    date_time = datetime.now().astimezone().strftime("%A, %B %d, %Y %H:%M:%S %Z")
    append_section = f"\n\n{append_system_prompt}" if append_system_prompt else ""

    if custom_prompt:
        prompt = custom_prompt
        prompt += append_section
        prompt += _format_project_context(context_files)

        has_read = True if selected_tools is None else ("read" in selected_tools)
        if has_read and skills:
            prompt += format_skills_for_prompt(skills)

        prompt += f"\nCurrent date and time: {date_time}"
        prompt += f"\nCurrent working directory: {cwd}"
        return prompt

    root = _find_repo_root(cwd)
    readme_path = str((root / "README.md").resolve())
    docs_path = str((root / "docs").resolve())
    examples_path = str((root / "examples").resolve())

    tool_source = selected_tools if selected_tools is not None else ["read", "bash", "edit", "write"]
    tools = [name for name in tool_source if name in TOOL_DESCRIPTIONS]
    tools_list = "\n".join(f"- {name}: {TOOL_DESCRIPTIONS[name]}" for name in tools) if tools else "(none)"

    has_bash = "bash" in tools
    has_edit = "edit" in tools
    has_write = "write" in tools
    has_grep = "grep" in tools
    has_find = "find" in tools
    has_ls = "ls" in tools
    has_read = "read" in tools

    guidelines: list[str] = []
    if has_bash and not (has_grep or has_find or has_ls):
        guidelines.append("Use bash for file operations like ls, rg, find")
    elif has_bash and (has_grep or has_find or has_ls):
        guidelines.append("Prefer grep/find/ls tools over bash for file exploration (faster, respects .gitignore)")
    if has_read and has_edit:
        guidelines.append("Use read to examine files before editing. You must use this tool instead of cat or sed.")
    if has_edit:
        guidelines.append("Use edit for precise changes (old text must match exactly)")
    if has_write:
        guidelines.append("Use write only for new files or complete rewrites")
    if has_edit or has_write:
        guidelines.append("When summarizing your actions, output plain text directly - do NOT use cat or bash to display what you did")
    guidelines.append("Be concise in your responses")
    guidelines.append("Show file paths clearly when working with files")
    guidelines_list = "\n".join(f"- {item}" for item in guidelines)

    prompt = f"""You are an expert coding assistant operating inside gen, a coding agent harness. You help users by reading files, executing commands, editing code, and writing new files.

Available tools:
{tools_list}

In addition to the tools above, you may have access to other custom tools depending on the project.

Guidelines:
{guidelines_list}

Gen documentation (read only when the user asks about gen itself, its SDK, extensions, themes, skills, or interactive UI):
- Main documentation: {readme_path}
- Additional docs: {docs_path}
- Examples: {examples_path} (extensions, custom tools, SDK)
- When asked about: extensions (docs/extensions.md, docs/extensions-migration.md, examples/extensions/), themes (docs/themes.md), skills (docs/skills.md), prompt templates (docs/prompt-templates.md), interactive keybindings and modes (README.md, docs/compatibility.md), SDK integrations (docs/sdk.md), custom providers (docs/custom-provider.md), adding models (docs/models.md), gen packages (docs/packages.md)
- When working on gen topics, read the docs and examples, and follow .md cross-references before implementing
- Always read gen .md files completely and follow links to related docs for interactive/runtime details"""

    prompt += append_section
    prompt += _format_project_context(context_files)
    if has_read and skills:
        prompt += format_skills_for_prompt(skills)
    prompt += f"\nCurrent date and time: {date_time}"
    prompt += f"\nCurrent working directory: {cwd}"
    return prompt
