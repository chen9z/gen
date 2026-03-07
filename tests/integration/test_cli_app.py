from pathlib import Path
import importlib

from typer.testing import CliRunner
import pytest

from gen_agent.runtime import SessionRuntime
from gen_agent.models.prompt import PromptInput

cli_module = importlib.import_module("gen_agent.cli.app")


def test_cli_continue_and_models_flags(tmp_path: Path, monkeypatch) -> None:
    session_dir = tmp_path / "sessions"
    seed = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )
    seed.set_model("anthropic", "claude-3-5-sonnet-latest")
    seed.set_thinking_level("low")
    seed_file = seed.session_file
    seed.set_session_name("seed")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        captured["session_file"] = session.session_file
        captured["scoped_models"] = list(session._scoped_model_patterns)
        captured["provider"] = session.provider_name
        captured["model"] = session.model_id
        captured["thinking"] = session.thinking_level
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)

    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--continue",
            "--models",
            "openai/*",
            "--session-dir",
            str(session_dir),
            "--cwd",
            str(tmp_path),
            "hello",
        ],
    )

    assert result.exit_code == 0, result.output
    assert captured["session_file"] == seed_file
    assert captured["scoped_models"] == ["openai/*"]
    assert captured["provider"] == "anthropic"
    assert captured["model"] == "claude-3-5-sonnet-latest"
    assert captured["thinking"] == "low"
    assert captured["message"] == "hello"


def test_cli_resume_requires_existing_previous_session(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--resume",
            "--session-dir",
            str(tmp_path / "sessions"),
            "--cwd",
            str(tmp_path),
            "hello",
        ],
    )
    assert result.exit_code != 0
    assert "No previous sessions found to resume" in result.output


def test_cli_extension_and_resource_flags(tmp_path: Path, monkeypatch) -> None:
    ext_file = tmp_path / "ext.py"
    ext_file.write_text(
        (
            "def register(pi):\n"
            "    def hello(args, session):\n"
            "        return None\n"
            '    pi.register_command("hello", hello, "hello cmd")\n'
        ),
        encoding="utf-8",
    )
    skill_dir = tmp_path / "skill-one"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: skill-one\ndescription: sample skill\n---\n# Skill",
        encoding="utf-8",
    )
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "hello.md").write_text("---\ndescription: hello\n---\nHello $1", encoding="utf-8")
    theme_dir = tmp_path / "themes"
    theme_dir.mkdir()
    (theme_dir / "custom.json").write_text('{"name":"custom","colors":{"ok":"green"}}', encoding="utf-8")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        captured["commands"] = sorted(session.extension_runner.get_commands().keys())
        captured["skills"] = [s.name for s in session.resource_loader.state.skills]
        captured["prompts"] = [p.name for p in session.resource_loader.state.prompts]
        captured["themes"] = [t.name for t in session.resource_loader.state.themes]
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()

    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--extension",
            str(ext_file),
            "--skill",
            str(skill_dir),
            "--prompt-template",
            str(prompt_dir),
            "--theme",
            str(theme_dir),
            "--cwd",
            str(tmp_path),
            "test",
        ],
    )
    assert result.exit_code == 0, result.output
    assert captured["commands"] == ["hello"]
    assert "skill-one" in captured["skills"]
    assert "hello" in captured["prompts"]
    assert "custom" in captured["themes"]
    assert captured["message"] == "test"

    result_no = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--extension",
            str(ext_file),
            "--no-extensions",
            "--skill",
            str(skill_dir),
            "--no-skills",
            "--prompt-template",
            str(prompt_dir),
            "--no-prompt-templates",
            "--theme",
            str(theme_dir),
            "--no-themes",
            "--cwd",
            str(tmp_path),
            "test",
        ],
    )
    assert result_no.exit_code == 0, result_no.output
    assert captured["commands"] == ["hello"]
    assert captured["skills"] == []
    assert captured["prompts"] == []
    assert captured["themes"] == []


def test_cli_extension_registered_flags(tmp_path: Path, monkeypatch) -> None:
    ext_file = tmp_path / "flags_ext.py"
    ext_file.write_text(
        (
            "def register(pi):\n"
            '    pi.register_flag("plan", "boolean", "enable plan mode")\n'
            '    pi.register_flag("persona", "string", "persona name")\n'
        ),
        encoding="utf-8",
    )

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        captured["flags"] = dict(session.extension_flags)
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--extension",
            str(ext_file),
            "--plan",
            "--persona",
            "strict",
            "--cwd",
            str(tmp_path),
            "hello",
        ],
    )

    assert result.exit_code == 0, result.output
    assert captured["flags"] == {"plan": True, "persona": "strict"}
    assert captured["message"] == "hello"


def test_cli_extension_string_flag_requires_value_before_next_option(tmp_path: Path, monkeypatch) -> None:
    ext_file = tmp_path / "flags_ext.py"
    ext_file.write_text(
        (
            "def register(pi):\n"
            '    pi.register_flag("persona", "string", "persona name")\n'
            '    pi.register_flag("plan", "boolean", "enable plan mode")\n'
        ),
        encoding="utf-8",
    )

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        del session, message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--extension",
            str(ext_file),
            "--persona",
            "--plan",
            "--cwd",
            str(tmp_path),
            "hello",
        ],
    )

    assert result.exit_code != 0
    assert "Missing value for --persona" in result.output


def test_cli_unknown_extra_option_fails(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "--unknown-flag",
            "hello",
        ],
    )
    assert result.exit_code != 0
    assert "Unknown option: --unknown-flag" in result.output


def test_cli_file_argument_expansion(tmp_path: Path, monkeypatch) -> None:
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("alpha\nbeta", encoding="utf-8")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        del session
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "@prompt.md",
            "summarize",
        ],
    )
    assert result.exit_code == 0, result.output
    msg = str(captured["message"])
    assert f'<file path="{prompt_file}">' in msg
    assert "alpha\nbeta" in msg
    assert "summarize" in msg


def test_cli_image_argument_expansion(tmp_path: Path, monkeypatch) -> None:
    image_file = tmp_path / "pic.png"
    image_file.write_bytes(b"\x89PNG\r\n\x1a\npayload")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message) -> int:
        del session
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "@pic.png",
            "describe",
        ],
    )
    assert result.exit_code == 0, result.output
    prompt = captured["message"]
    assert isinstance(prompt, PromptInput)
    assert prompt.text == "describe"
    assert len(prompt.images) == 1
    assert prompt.images[0].mime_type == "image/png"
    assert prompt.images[0].data


def test_cli_only_image_argument_yields_prompt_input(tmp_path: Path, monkeypatch) -> None:
    image_file = tmp_path / "noext"
    image_file.write_bytes(b"\x89PNG\r\n\x1a\npayload")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message) -> int:
        del session
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "@noext",
        ],
    )
    assert result.exit_code == 0, result.output
    prompt = captured["message"]
    assert isinstance(prompt, PromptInput)
    assert prompt.text == ""
    assert len(prompt.images) == 1
    assert prompt.images[0].mime_type == "image/png"


def test_cli_system_prompt_options(tmp_path: Path, monkeypatch) -> None:
    append_file = tmp_path / "append.txt"
    append_file.write_text("Append from file.", encoding="utf-8")
    agents_file = tmp_path / "AGENTS.md"
    agents_file.write_text("# Context\nAlways run tests.", encoding="utf-8")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        captured["system_prompt"] = session._build_system_prompt()
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "--system-prompt",
            "Base system prompt",
            "--append-system-prompt",
            str(append_file),
            "hello",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Base system prompt" in str(captured["system_prompt"])
    assert "Append from file." in str(captured["system_prompt"])
    assert str(agents_file) in str(captured["system_prompt"])
    assert "Always run tests." in str(captured["system_prompt"])
    assert f"Current working directory: {tmp_path}" in str(captured["system_prompt"])
    assert captured["message"] == "hello"


def test_cli_list_models_output(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--list-models",
            "--cwd",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Available models:" in result.output
    assert "openai/gpt-4o-mini" in result.output

    filtered = runner.invoke(
        cli_module.app,
        [
            "--list-models",
            "--list-models-search",
            "haiku",
            "--cwd",
            str(tmp_path),
        ],
    )
    assert filtered.exit_code == 0, filtered.output
    assert "anthropic/claude-3-5-haiku-latest" in filtered.output
    assert "openai/gpt-4o-mini" not in filtered.output


def test_cli_list_models_uses_models_json_catalog(tmp_path: Path) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"custom":{"baseUrl":"https://custom.local/v1","apiKey":"CUSTOM_KEY","api":"openai-completions","models":[{"id":"alpha-1"},{"id":"beta-2"}]}'
            "}"
            "}"
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--list-models",
            "--cwd",
            str(tmp_path),
        ],
        env={"XDG_CONFIG_HOME": str(xdg)},
    )
    assert result.exit_code == 0, result.output
    assert "custom/alpha-1" in result.output
    assert "custom/beta-2" in result.output


def test_cli_list_models_shows_merged_registry_view(tmp_path: Path) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"openai":{"baseUrl":"https://proxy.openai.local/v1","apiKey":"OPENAI_PROXY_KEY","api":"openai-completions","models":[{"id":"gpt-4o-mini","reasoning":false},{"id":"proxy-only","reasoning":false}]}'
            "}"
            "}"
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--list-models",
            "--cwd",
            str(tmp_path),
        ],
        env={"XDG_CONFIG_HOME": str(xdg)},
    )
    assert result.exit_code == 0, result.output
    assert "openai/gpt-4o-mini" in result.output
    assert "openai/gpt-4o" in result.output
    assert "openai/proxy-only" in result.output


def test_cli_model_thinking_clamped_by_model_capability(tmp_path: Path, monkeypatch) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"openai":{"baseUrl":"https://proxy.openai.local/v1","apiKey":"OPENAI_PROXY_KEY","api":"openai-completions","models":[{"id":"gpt-4o-mini","reasoning":false}]}'
            "}"
            "}"
        ),
        encoding="utf-8",
    )

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | None = None) -> int:
        captured["provider"] = session.provider_name
        captured["model"] = session.model_id
        captured["thinking"] = session.thinking_level
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "--model",
            "openai/gpt-4o-mini:high",
            "hello",
        ],
        env={"XDG_CONFIG_HOME": str(xdg)},
    )
    assert result.exit_code == 0, result.output
    assert captured["provider"] == "openai"
    assert captured["model"] == "gpt-4o-mini"
    assert captured["thinking"] == "off"
    assert captured["message"] == "hello"


def test_cli_list_models_shows_thinking_capability(tmp_path: Path) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        (
            '{'
            '"providers":{'
            '"custom":{"baseUrl":"https://custom.local/v1","apiKey":"CUSTOM_KEY","api":"openai-completions","models":[{"id":"alpha-1","reasoning":false},{"id":"beta-2","reasoning":true}]}'
            "}"
            "}"
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--list-models",
            "--cwd",
            str(tmp_path),
        ],
        env={"XDG_CONFIG_HOME": str(xdg)},
    )
    assert result.exit_code == 0, result.output
    assert "custom/alpha-1 (thinking: no)" in result.output
    assert "custom/beta-2 (thinking: yes)" in result.output


def test_cli_continue_allows_empty_prompt_in_print_and_json(tmp_path: Path, monkeypatch) -> None:
    session_dir = tmp_path / "sessions"
    seed = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )
    seed.set_session_name("seed")

    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | None = None) -> int:
        captured["print_session"] = session.session_file
        captured["print_message"] = message
        return 0

    async def fake_run_json_mode(session: SessionRuntime, message: str | None = None) -> int:
        captured["json_session"] = session.session_file
        captured["json_message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    monkeypatch.setattr(cli_module, "run_json_mode", fake_run_json_mode)

    runner = CliRunner()
    print_result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--continue",
            "--session-dir",
            str(session_dir),
            "--cwd",
            str(tmp_path),
        ],
    )
    assert print_result.exit_code == 0, print_result.output
    assert captured["print_message"] is None
    assert captured["print_session"] == seed.session_file

    json_result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "json",
            "--continue",
            "--session-dir",
            str(session_dir),
            "--cwd",
            str(tmp_path),
        ],
    )
    assert json_result.exit_code == 0, json_result.output
    assert captured["json_message"] is None
    assert captured["json_session"] != seed.session_file
    assert str(captured["json_session"]).endswith(".jsonl")


def test_cli_rejects_unknown_tools(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--tools",
            "read,missing_tool",
            "--cwd",
            str(tmp_path),
            "hello",
        ],
    )
    assert result.exit_code != 0
    assert "Unknown tool(s): missing_tool" in result.output


def test_cli_model_with_thinking_suffix(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | None = None) -> int:
        captured["provider"] = session.provider_name
        captured["model"] = session.model_id
        captured["thinking"] = session.thinking_level
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "--model",
            "openai/gpt-4o:high",
            "hello",
        ],
        env={"XDG_CONFIG_HOME": str(tmp_path / "xdg")},
    )
    assert result.exit_code == 0, result.output
    assert captured["provider"] == "openai"
    assert captured["model"] == "gpt-4o"
    assert captured["thinking"] == "high"
    assert captured["message"] == "hello"


def test_cli_model_fuzzy_lookup(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | None = None) -> int:
        captured["provider"] = session.provider_name
        captured["model"] = session.model_id
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "--model",
            "haiku",
            "hello",
        ],
    )
    assert result.exit_code == 0, result.output
    assert captured["provider"] == "anthropic"
    assert captured["model"] == "claude-3-5-haiku-latest"
    assert captured["message"] == "hello"


def test_cli_reads_piped_stdin_for_print_mode(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | None = None) -> int:
        del session
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
        ],
        input="from stdin\n",
    )
    assert result.exit_code == 0, result.output
    assert captured["message"] == "from stdin"


def test_cli_piped_stdin_defaults_to_print_mode(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | None = None) -> int:
        del session
        captured["mode"] = "print"
        captured["message"] = message
        return 0

    async def fake_run_interactive_mode(session: SessionRuntime, initial_message: str | None = None) -> int:
        del session, initial_message
        raise AssertionError("interactive mode should not be selected for piped stdin")

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    monkeypatch.setattr(cli_module, "run_interactive_mode", fake_run_interactive_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--cwd",
            str(tmp_path),
        ],
        input="hello from pipe\n",
    )
    assert result.exit_code == 0, result.output
    assert captured["mode"] == "print"
    assert captured["message"] == "hello from pipe"


def test_cli_print_mode_nonzero_on_provider_error(tmp_path: Path) -> None:
    isolated_home = tmp_path / "home"
    isolated_xdg = tmp_path / "xdg"
    isolated_home.mkdir(parents=True, exist_ok=True)
    isolated_xdg.mkdir(parents=True, exist_ok=True)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--provider",
            "openai",
            "--no-session",
            "--cwd",
            str(tmp_path),
            "hello",
        ],
        env={
            "OPENAI_API_KEY": "",
            "ANTHROPIC_API_KEY": "",
            "HOME": str(isolated_home),
            "XDG_CONFIG_HOME": str(isolated_xdg),
        },
    )
    assert result.exit_code == 1
    assert "No API key for provider openai" in result.output


@pytest.mark.asyncio
async def test_print_mode_outputs_only_last_assistant_for_multiple_prompts(tmp_path: Path, capsys) -> None:
    class SeqProvider:
        def __init__(self) -> None:
            self.i = 0

        async def complete(self, request):
            self.i += 1
            return importlib.import_module("gen_agent.models.messages").AssistantMessage(
                provider=request.provider,
                model=request.model_id,
                content=[importlib.import_module("gen_agent.models.content").TextContent(text=f"r{self.i}")],
                stopReason="stop",
            )

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = SeqProvider()

    code = await importlib.import_module("gen_agent.modes.print_mode").run_print_mode(session, ["a", "b"])
    assert code == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert out[-1] == "r2"
    assert "r1" not in out


def test_cli_list_models_accepts_positional_search(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--list-models",
            "haiku",
            "--cwd",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "anthropic/claude-3-5-haiku-latest" in result.output
    assert "openai/gpt-4o-mini" not in result.output


def test_cli_multiple_messages_passed_as_sequence(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str | list[str] | None = None) -> int:
        del session
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--cwd",
            str(tmp_path),
            "first",
            "second",
        ],
    )
    assert result.exit_code == 0, result.output
    assert captured["message"] == ["first", "second"]


def test_cli_models_applies_scoped_startup_model_and_thinking(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_run_print_mode(session: SessionRuntime, message: str) -> int:
        captured["provider"] = session.provider_name
        captured["model"] = session.model_id
        captured["thinking"] = session.thinking_level
        captured["message"] = message
        return 0

    monkeypatch.setattr(cli_module, "run_print_mode", fake_run_print_mode)
    isolated_home = tmp_path / "home"
    isolated_xdg = tmp_path / "xdg"
    isolated_home.mkdir(parents=True, exist_ok=True)
    isolated_xdg.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        cli_module.app,
        [
            "--mode",
            "print",
            "--models",
            "anthropic/*:low",
            "--cwd",
            str(tmp_path),
            "hello",
        ],
        env={
            "HOME": str(isolated_home),
            "XDG_CONFIG_HOME": str(isolated_xdg),
        },
    )

    assert result.exit_code == 0, result.output
    assert captured["provider"] == "anthropic"
    assert captured["model"] == "claude-3-5-sonnet-latest"
    assert captured["thinking"] == "low"
    assert captured["message"] == "hello"
