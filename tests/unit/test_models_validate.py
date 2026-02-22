from pydantic import TypeAdapter
import pytest

from gen_agent.models.events import AgentEvent, AgentSessionEvent
from gen_agent.models.messages import AgentMessage, AssistantMessage, UserMessage
from gen_agent.models.rpc import RpcCommand, RpcResponse
from gen_agent.models.session import FileEntry
from gen_agent.models.settings import SettingsModel
from gen_agent.models.tools import BashInput, EditInput, FindInput, GrepInput, LsInput, ReadInput, ToolResult, WriteInput


def test_message_union_validation() -> None:
    adapter = TypeAdapter(AgentMessage)
    msg = adapter.validate_python({"role": "user", "content": "hello", "timestamp": 1})
    assert isinstance(msg, UserMessage)


def test_event_union_validation() -> None:
    adapter = TypeAdapter(AgentEvent)
    event = adapter.validate_python({"type": "agent_start"})
    assert event.type == "agent_start"


def test_session_event_union_validation() -> None:
    adapter = TypeAdapter(AgentSessionEvent)
    event = adapter.validate_python({"type": "auto_retry_end", "success": True, "attempt": 1})
    assert event.type == "auto_retry_end"


def test_file_entry_union_validation() -> None:
    adapter = TypeAdapter(FileEntry)
    header = adapter.validate_python(
        {"type": "session", "id": "s", "timestamp": "2026-01-01T00:00:00Z", "cwd": "/tmp"}
    )
    assert header.type == "session"


def test_rpc_models_validation() -> None:
    adapter = TypeAdapter(RpcCommand)
    cmd = adapter.validate_python({"type": "prompt", "message": "hi"})
    assert cmd.type == "prompt"
    assert adapter.validate_python({"type": "continue"}).type == "continue"
    assert adapter.validate_python({"type": "cycle_model"}).type == "cycle_model"
    assert adapter.validate_python({"type": "set_thinking_level", "level": "medium"}).type == "set_thinking_level"
    assert adapter.validate_python({"type": "set_steering_mode", "mode": "all"}).type == "set_steering_mode"
    assert adapter.validate_python({"type": "set_follow_up_mode", "mode": "one-at-a-time"}).type == "set_follow_up_mode"
    assert adapter.validate_python({"type": "set_session_name", "name": "demo"}).type == "set_session_name"
    assert adapter.validate_python({"type": "get_tree"}).type == "get_tree"
    assert adapter.validate_python({"type": "switch_tree", "leafId": "abc"}).type == "switch_tree"
    assert adapter.validate_python({"type": "list_sessions", "limit": 10}).type == "list_sessions"
    assert adapter.validate_python({"type": "resume_session", "index": 1}).type == "resume_session"
    assert adapter.validate_python({"type": "fork_session"}).type == "fork_session"
    assert adapter.validate_python({"type": "compact"}).type == "compact"
    assert adapter.validate_python({"type": "reload"}).type == "reload"

    resp = RpcResponse(command="prompt", success=True)
    assert resp.success is True


def test_settings_model_validation() -> None:
    model = SettingsModel.model_validate({"defaultProvider": "openai", "retry": {"maxRetries": 5}})
    assert model.default_provider == "openai"
    assert model.retry.max_retries == 5


def test_tool_models_validation() -> None:
    ReadInput.model_validate({"path": "a.txt", "offset": 1, "limit": 10})
    WriteInput.model_validate({"path": "a.txt", "content": "x"})
    EditInput.model_validate({"path": "a.txt", "oldText": "a", "newText": "b"})
    BashInput.model_validate({"command": "echo 1", "timeout": 3})
    GrepInput.model_validate({"pattern": "foo", "path": "."})
    FindInput.model_validate({"glob": "*.py"})
    LsInput.model_validate({"path": ".", "recursive": True})
    ToolResult.model_validate({"content": [{"type": "text", "text": "ok"}], "details": None})


def test_tool_models_validation_rejects_invalid_numeric_bounds() -> None:
    with pytest.raises(Exception):
        ReadInput.model_validate({"path": "a.txt", "offset": 0})
    with pytest.raises(Exception):
        BashInput.model_validate({"command": "echo 1", "timeout": 0})
    with pytest.raises(Exception):
        GrepInput.model_validate({"pattern": "x", "limit": 0})
    with pytest.raises(Exception):
        FindInput.model_validate({"pattern": "*.py", "limit": 0})
    with pytest.raises(Exception):
        LsInput.model_validate({"path": ".", "limit": 0})


def test_assistant_message_usage_aliases() -> None:
    msg = AssistantMessage(
        content=[{"type": "text", "text": "ok"}],
        provider="openai",
        model="gpt-4o-mini",
        usage={"input": 1, "output": 2, "totalTokens": 3, "cost": {"total": 0.0}},
    )
    dumped = msg.model_dump(by_alias=True)
    assert dumped["usage"]["totalTokens"] == 3
