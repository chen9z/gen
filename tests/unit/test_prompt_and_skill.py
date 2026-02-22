from pathlib import Path

from gen_agent.resources.loader import ResourceLoader
from gen_agent.resources.prompts import expand_prompt_template, load_prompt_templates, parse_command_args
from gen_agent.resources.skills import load_skills


def test_prompt_template_substitution(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "hello.md").write_text("---\ndescription: test\n---\nHello $1 $ARGUMENTS", encoding="utf-8")

    templates, diagnostics = load_prompt_templates([str(prompt_dir)])
    expanded = expand_prompt_template("/hello world from test", templates)
    assert "Hello world world from test" in expanded
    assert diagnostics == []


def test_skill_frontmatter_validation(tmp_path: Path) -> None:
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: test skill\n---\n# body", encoding="utf-8")

    skills, diagnostics = load_skills([str(tmp_path)])
    assert len(skills) == 1
    assert skills[0].name == "my-skill"
    assert diagnostics == []


def test_prompt_template_collision_diagnostics(tmp_path: Path) -> None:
    one = tmp_path / "one"
    two = tmp_path / "two"
    one.mkdir()
    two.mkdir()
    (one / "dup.md").write_text("---\ndescription: a\n---\nA", encoding="utf-8")
    (two / "dup.md").write_text("---\ndescription: b\n---\nB", encoding="utf-8")

    templates, diagnostics = load_prompt_templates([str(one), str(two)])
    assert len(templates) == 1
    assert any("prompt name collision: dup" in line for line in diagnostics)


def test_context_file_priority_and_global_loading(tmp_path: Path, monkeypatch) -> None:
    xdg = tmp_path / "xdg"
    global_ctx_dir = xdg / "gen-agent"
    global_ctx_dir.mkdir(parents=True, exist_ok=True)
    (global_ctx_dir / "CLAUDE.md").write_text("global-claude", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))

    parent = tmp_path / "repo"
    child = parent / "src"
    child.mkdir(parents=True, exist_ok=True)
    (parent / "CLAUDE.md").write_text("parent-claude", encoding="utf-8")
    (parent / "AGENTS.md").write_text("parent-agents", encoding="utf-8")
    (child / "AGENTS.md").write_text("child-agents", encoding="utf-8")

    loader = ResourceLoader(str(child))
    state = loader.reload()
    context_files = state.context_files
    paths = [p for p, _c in context_files]
    contents = [c for _p, c in context_files]

    assert str(global_ctx_dir / "CLAUDE.md") in paths
    assert str(parent / "AGENTS.md") in paths
    assert str(parent / "CLAUDE.md") not in paths
    assert "global-claude" in contents
    assert "parent-agents" in contents


def test_parse_command_args_shlex_compatible() -> None:
    args = parse_command_args(r'''one "two words" 'three four' five\ six''')
    assert args == ["one", "two words", "three four", "five six"]
