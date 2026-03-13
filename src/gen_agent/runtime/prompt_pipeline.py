from __future__ import annotations

from pathlib import Path

from gen_agent.models.content import ImageContent, TextContent
from gen_agent.models.messages import UserMessage
from gen_agent.resources.frontmatter import parse_frontmatter


class PromptPipeline:
    def __init__(self, *, resource_loader, skill_commands_enabled: bool) -> None:
        self._resource_loader = resource_loader
        self._skill_commands_enabled = skill_commands_enabled

    def update_skill_commands_enabled(self, enabled: bool) -> None:
        self._skill_commands_enabled = enabled

    def expand_prompt(self, text: str) -> str:
        expanded = self._expand_skill_command(text)
        return self._resource_loader.expand_prompt(expanded)

    def build_user_message(self, message: str, images: list[ImageContent]) -> UserMessage:
        if not images:
            return UserMessage(content=message)
        return UserMessage(content=[TextContent(text=message), *images])

    def _expand_skill_command(self, text: str) -> str:
        if not text.startswith("/skill:") or not self._skill_commands_enabled:
            return text

        command_part, _, args = text.partition(" ")
        skill_name = command_part[7:]
        skill = next((item for item in self._resource_loader.state.skills if item.name == skill_name), None)
        if not skill:
            return text
        try:
            raw = Path(skill.file_path).read_text(encoding="utf-8")
            _meta, body = parse_frontmatter(raw)
            skill_block = (
                f'<skill name="{skill.name}" location="{skill.file_path}">\n'
                f"References are relative to {skill.base_dir}.\n\n"
                f"{body.strip()}\n"
                "</skill>"
            )
            suffix = args.strip()
            return f"{skill_block}\n\n{suffix}" if suffix else skill_block
        except Exception:
            return text
