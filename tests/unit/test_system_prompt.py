from gen_agent.core.system_prompt import build_system_prompt
from gen_agent.resources.skills import Skill


def _skill() -> Skill:
    return Skill(
        name="demo-skill",
        description="demo",
        file_path="/tmp/demo/SKILL.md",
        base_dir="/tmp/demo",
        source="path",
        disable_model_invocation=False,
    )


def test_system_prompt_empty_tools_shows_none_and_paths() -> None:
    prompt = build_system_prompt(
        cwd="/tmp",
        custom_prompt=None,
        selected_tools=[],
        append_system_prompt=None,
        context_files=[],
        skills=[],
    )
    assert "Available tools:\n(none)" in prompt
    assert "Show file paths clearly when working with files" in prompt


def test_system_prompt_default_tools_included() -> None:
    prompt = build_system_prompt(
        cwd="/tmp",
        custom_prompt=None,
        selected_tools=["read", "bash", "edit", "write"],
        append_system_prompt=None,
        context_files=[],
        skills=[],
    )
    assert "- read:" in prompt
    assert "- bash:" in prompt
    assert "- edit:" in prompt
    assert "- write:" in prompt


def test_system_prompt_custom_prompt_branch_appends_context_and_append_text() -> None:
    prompt = build_system_prompt(
        cwd="/tmp",
        custom_prompt="Base prompt",
        selected_tools=["read"],
        append_system_prompt="Append block",
        context_files=[("/tmp/AGENTS.md", "ctx")],
        skills=[],
    )
    assert "Base prompt" in prompt
    assert "Append block" in prompt
    assert "## /tmp/AGENTS.md" in prompt
    assert "ctx" in prompt
    assert "Current working directory: /tmp" in prompt


def test_system_prompt_skills_requires_read_tool() -> None:
    with_read = build_system_prompt(
        cwd="/tmp",
        custom_prompt=None,
        selected_tools=["read"],
        append_system_prompt=None,
        context_files=[],
        skills=[_skill()],
    )
    without_read = build_system_prompt(
        cwd="/tmp",
        custom_prompt=None,
        selected_tools=["bash"],
        append_system_prompt=None,
        context_files=[],
        skills=[_skill()],
    )
    assert "<available_skills>" in with_read
    assert "<available_skills>" not in without_read
