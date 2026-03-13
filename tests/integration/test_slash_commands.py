from pathlib import Path
import os
import time

import pytest

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage, UserMessage
from gen_agent.runtime import SessionRuntime


class PlainProvider:
    async def complete(self, request):
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="ok")],
            stopReason="stop",
        )


@pytest.mark.asyncio
async def test_compact_tree_and_settings_commands(tmp_path: Path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    for i in range(5):
        session.session_manager.append_message(UserMessage(content=f"m{i}"))

    compact_resp = await session.prompt("/compact")
    assert "Manual compaction completed" in compact_resp[-1].content[0].text
    assert any(entry.type == "compaction" for entry in session.session_manager.entries)

    tree_resp = await session.prompt("/tree")
    assert "Tree entries" in tree_resp[-1].content[0].text
    tree_switch = await session.prompt("/tree 1")
    assert "Moved tree leaf to #1" in tree_switch[-1].content[0].text

    set_resp = await session.prompt('/settings set retry.maxRetries 7 project')
    assert "Updated project setting" in set_resp[-1].content[0].text

    get_resp = await session.prompt('/settings get retry.maxRetries')
    assert "retry.maxRetries" in get_resp[-1].content[0].text

    hotkeys_resp = await session.prompt("/hotkeys")
    assert "Ctrl+P" in hotkeys_resp[-1].content[0].text

    model_resp = await session.prompt("/model openai/gpt-4o:low")
    assert "Model set to openai/gpt-4o" in model_resp[-1].content[0].text
    assert session.model_id == "gpt-4o"
    assert session.thinking_level == "low"

    fuzzy_resp = await session.prompt("/model haiku")
    assert "Model set to anthropic/claude-3-5-haiku-latest" in fuzzy_resp[-1].content[0].text
    assert session.provider_name == "anthropic"
    assert session.model_id == "claude-3-5-haiku-latest"


@pytest.mark.asyncio
async def test_fork_resume_and_scoped_models_commands(tmp_path: Path):
    session_dir = tmp_path / "sessions"
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    await session.prompt("/name base")
    base_file = session.session_file

    fork_resp = await session.prompt("/fork")
    assert "Forked session to" in fork_resp[-1].content[0].text
    assert session.session_file != base_file
    assert any(entry.type == "branch_summary" for entry in session.session_manager.entries)

    resume_list = await session.prompt("/resume")
    assert "Recent sessions" in resume_list[-1].content[0].text
    assert "*" in resume_list[-1].content[0].text

    resume_one = await session.prompt("/resume 1")
    assert "Resumed session" in resume_one[-1].content[0].text

    invalid_fork = await session.prompt("/fork missing-id")
    assert "Unknown entry id: missing-id" in invalid_fork[-1].content[0].text

    scoped = await session.prompt("/scoped-models openai/*")
    assert "Scoped models updated" in scoped[-1].content[0].text

    before = session.model_id
    session.cycle_model()
    assert session.provider_name == "openai"
    assert session.model_id != ""
    assert session.model_id != before or session.model_id == "gpt-4o-mini"


@pytest.mark.asyncio
async def test_resume_restores_model_and_thinking_from_session(tmp_path: Path):
    session_dir = tmp_path / "sessions"
    base = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )
    base.provider_registry._providers["openai"] = PlainProvider()
    await base.prompt("/model anthropic/claude-3-5-sonnet-latest:low")
    target_file = base.session_file

    other = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )
    other.provider_registry._providers["openai"] = PlainProvider()
    assert other.provider_name == "openai"
    assert other.model_id == "gpt-4o-mini"

    resumed = other.resume_session(target_file)
    assert resumed == target_file
    assert other.provider_name == "anthropic"
    assert other.model_id == "claude-3-5-sonnet-latest"
    assert other.thinking_level == "low"


@pytest.mark.asyncio
async def test_reload_rebuilds_extension_tools(tmp_path: Path):
    ext_file = tmp_path / "ext.py"
    ext_file.write_text(
        (
            "from pydantic import BaseModel\n"
            "from gen_agent.models.content import TextContent\n"
            "from gen_agent.tools.base import Tool\n\n"
            "class Input(BaseModel):\n"
            "    pass\n\n"
            "class ToolA(Tool):\n"
            '    name = "tool_a"\n'
            '    label = "Tool A"\n'
            '    description = "A"\n'
            "    input_model = Input\n"
            "    async def execute(self, params):\n"
            "        del params\n"
            '        return [TextContent(text="a")], None\n\n'
            "def register(pi):\n"
            "    pi.register_tool(ToolA())\n"
        ),
        encoding="utf-8",
    )

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
        extensions=[str(ext_file)],
    )
    session.provider_registry._providers["openai"] = PlainProvider()
    assert "tool_a" in session.available_tools

    ext_file.write_text(
        (
            "from pydantic import BaseModel\n"
            "from gen_agent.models.content import TextContent\n"
            "from gen_agent.tools.base import Tool\n\n"
            "class Input(BaseModel):\n"
            "    pass\n\n"
            "class ToolB(Tool):\n"
            '    name = "tool_b"\n'
            '    label = "Tool B"\n'
            '    description = "B"\n'
            "    input_model = Input\n"
            "    async def execute(self, params):\n"
            "        del params\n"
            '        return [TextContent(text="b")], None\n\n'
            "def register(pi):\n"
            "    pi.register_tool(ToolB())\n"
        ),
        encoding="utf-8",
    )
    now = time.time() + 2.0
    os.utime(ext_file, (now, now))

    reload_resp = await session.prompt("/reload")
    assert "Reloaded resources" in reload_resp[-1].content[0].text
    assert "tool_b" in session.available_tools
    assert "tool_a" not in session.available_tools


@pytest.mark.asyncio
async def test_reload_reports_resource_diagnostics(tmp_path: Path):
    prompt_a = tmp_path / "prompts_a"
    prompt_b = tmp_path / "prompts_b"
    prompt_a.mkdir()
    prompt_b.mkdir()
    (prompt_a / "dup.md").write_text("---\ndescription: a\n---\nA", encoding="utf-8")
    (prompt_b / "dup.md").write_text("---\ndescription: b\n---\nB", encoding="utf-8")

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
        prompt_templates=[str(prompt_a), str(prompt_b)],
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    resp = await session.prompt("/reload")
    text = resp[-1].content[0].text
    assert "Reloaded resources" in text
    assert "prompt name collision: dup" in text


@pytest.mark.asyncio
async def test_scoped_models_with_thinking_and_unmatched_pattern(tmp_path: Path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    scoped = await session.prompt("/scoped-models openai/gpt-4o:high,missing-model")
    scoped_text = scoped[-1].content[0].text
    assert "Scoped models updated:" in scoped_text
    assert "openai/gpt-4o:high" in scoped_text
    assert 'No models match pattern "missing-model"' in scoped_text

    session.set_thinking_level("low")
    result = session.cycle_model()
    assert result["isScoped"] is True
    assert session.provider_name == "openai"
    assert session.model_id == "gpt-4o"
    assert session.thinking_level == "high"


@pytest.mark.asyncio
async def test_scoped_models_invalid_thinking_suffix_warns_and_falls_back(tmp_path: Path):
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    resp = await session.prompt("/scoped-models openai/gpt-4o:ultra")
    text = resp[-1].content[0].text
    assert 'Invalid thinking level "ultra"' in text
    assert "openai/gpt-4o:off" in text


@pytest.mark.asyncio
async def test_model_command_clamps_thinking_for_non_reasoning_model(tmp_path: Path, monkeypatch):
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
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    await session.prompt("/model openai/gpt-4o-mini:high")
    assert session.thinking_level == "off"


@pytest.mark.asyncio
async def test_cycle_model_prefers_providers_with_auth(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    session.set_scoped_models(["openai/*", "anthropic/*"])
    for _ in range(6):
        data = session.cycle_model()
        assert data["provider"] == "openai"


@pytest.mark.asyncio
async def test_extension_event_handlers_receive_agent_events(tmp_path: Path):
    ext_file = tmp_path / "event_ext.py"
    ext_file.write_text(
        (
            "def register(pi):\n"
            "    def on_agent_start(payload, session):\n"
            "        session._ext_agent_start = payload.get('type')\n"
            "    def on_agent_end(payload, session):\n"
            "        session._ext_agent_end_count = getattr(session, '_ext_agent_end_count', 0) + 1\n"
            "    pi.on('agent_start', on_agent_start)\n"
            "    pi.on('agent_end', on_agent_end)\n"
        ),
        encoding="utf-8",
    )

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
        extensions=[str(ext_file)],
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    await session.prompt("hello")
    assert getattr(session, "_ext_agent_start", None) == "agent_start"
    assert getattr(session, "_ext_agent_end_count", 0) == 1


@pytest.mark.asyncio
async def test_extension_command_return_value_is_used(tmp_path: Path):
    ext_file = tmp_path / "cmd_ext.py"
    ext_file.write_text(
        (
            "def register(pi):\n"
            "    def hello(args, session):\n"
            "        session._ext_cmd_session_ok = session is not None\n"
            "        return f'hello:{args}'\n"
            "    pi.register_command('hello', hello, 'hello cmd')\n"
        ),
        encoding="utf-8",
    )

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
        extensions=[str(ext_file)],
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    resp = await session.prompt("/hello world")
    assert resp[-1].content[0].text == "hello:world"
    assert getattr(session, "_ext_cmd_session_ok", False) is True


@pytest.mark.asyncio
async def test_extension_command_async_handler_supported(tmp_path: Path):
    ext_file = tmp_path / "cmd_async_ext.py"
    ext_file.write_text(
        (
            "import asyncio\n"
            "def register(pi):\n"
            "    async def hello(args, session):\n"
            "        await asyncio.sleep(0)\n"
            "        return f'async:{args}'\n"
            "    pi.register_command('hello_async', hello, 'hello async')\n"
        ),
        encoding="utf-8",
    )

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
        extensions=[str(ext_file)],
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    resp = await session.prompt("/hello_async world")
    assert resp[-1].content[0].text == "async:world"


@pytest.mark.asyncio
async def test_skill_command_expands_to_user_prompt(tmp_path: Path):
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: my-skill\ndescription: demo skill\n---\n# Steps\nUse rg first.",
        encoding="utf-8",
    )

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
        skills=[str(skill_dir)],
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    msgs = await session.prompt("/skill:my-skill fix this bug")
    user_msg = msgs[0]
    assert user_msg.role == "user"
    assert "References are relative to" in user_msg.content
    assert "Use rg first." in user_msg.content
    assert "fix this bug" in user_msg.content
