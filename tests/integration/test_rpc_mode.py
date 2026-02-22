import asyncio
import json
import threading

import pytest

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage
from gen_agent.modes.rpc_mode import RpcMode


class PlainProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def complete(self, request):
        self.calls += 1
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="rpc-ok")],
            stopReason="stop",
        )


class SlowProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def complete(self, request):
        self.calls += 1
        await asyncio.sleep(10)
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="slow-ok")],
            stopReason="stop",
        )


class _BlockingStdin:
    def __init__(self, first_line: str) -> None:
        self._first_line = first_line
        self._sent = False
        self._release = threading.Event()

    def readline(self) -> str:
        if not self._sent:
            self._sent = True
            return self._first_line + "\n"
        self._release.wait(timeout=5)
        return ""

    def release(self) -> None:
        self._release.set()


@pytest.mark.asyncio
async def test_rpc_get_state_and_prompt(tmp_path):
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.provider_registry._providers["openai"] = PlainProvider()

    rpc = RpcMode(session)
    output = []
    rpc._write = lambda payload: output.append(payload)

    await rpc._handle({"type": "get_state", "id": "1"})
    await rpc._handle({"type": "prompt", "id": "2", "message": "hello"})

    assert output[0]["command"] == "get_state"
    assert output[0]["data"]["steeringMode"] in {"all", "one-at-a-time"}
    assert output[0]["data"]["followUpMode"] in {"all", "one-at-a-time"}
    assert "sessionId" in output[0]["data"]
    assert output[1]["command"] == "prompt"
    assert output[1]["success"] is True


@pytest.mark.asyncio
async def test_rpc_extended_commands(tmp_path):
    session_dir = tmp_path / "sessions"
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )
    provider = PlainProvider()
    session.provider_registry._providers["openai"] = provider

    rpc = RpcMode(session)
    output = []
    rpc._write = lambda payload: output.append(payload)

    base_file = session.session_file
    await rpc._handle({"type": "prompt", "id": "p1", "message": "hello"})
    await rpc._handle({"type": "set_session_name", "id": "n1", "name": "base"})
    await rpc._handle({"type": "get_tree", "id": "t1"})
    tree_resp = output[-1]
    first_entry_id = tree_resp["data"]["entries"][0]["id"]
    assert tree_resp["success"] is True
    assert tree_resp["data"]["leafId"]

    await rpc._handle({"type": "switch_tree", "id": "t2", "leafId": first_entry_id})
    assert output[-1]["success"] is True
    await rpc._handle({"type": "switch_tree", "id": "t3", "leafId": "missing"})
    assert output[-1]["success"] is False

    await rpc._handle({"type": "set_thinking_level", "id": "th1", "level": "low"})
    await rpc._handle({"type": "set_steering_mode", "id": "sm1", "mode": "all"})
    await rpc._handle({"type": "set_follow_up_mode", "id": "fm1", "mode": "one-at-a-time"})
    await rpc._handle({"type": "cycle_model", "id": "cm1"})
    await rpc._handle({"type": "continue", "id": "co1"})
    assert output[-5]["command"] == "set_thinking_level"
    assert output[-4]["command"] == "set_steering_mode"
    assert output[-3]["command"] == "set_follow_up_mode"
    assert output[-5]["success"] is True
    assert output[-4]["success"] is True
    assert output[-3]["success"] is True
    assert output[-2]["command"] == "cycle_model"
    assert output[-1]["command"] == "continue"

    await rpc._handle({"type": "list_sessions", "id": "ls1", "limit": 10})
    list_resp = output[-1]
    assert list_resp["success"] is True
    assert list_resp["data"]["sessions"]

    await rpc._handle({"type": "fork_session", "id": "f1"})
    fork_resp = output[-1]
    fork_file = fork_resp["data"]["sessionFile"]
    assert fork_resp["success"] is True
    assert fork_file and fork_file != base_file
    await rpc._handle({"type": "fork_session", "id": "f2", "leafId": "missing"})
    assert output[-1]["success"] is False
    assert "Unknown tree leaf" in output[-1]["error"]

    await rpc._handle({"type": "resume_session", "id": "r1", "path": base_file})
    assert output[-1]["success"] is True
    assert session.session_file == base_file

    await rpc._handle({"type": "compact", "id": "c1"})
    compact_resp = output[-1]
    assert compact_resp["success"] is True
    assert "compaction" in compact_resp["data"]["message"].lower()

    await rpc._handle({"type": "reload", "id": "re1"})
    assert output[-1]["success"] is True
    assert "diagnostics" in output[-1]["data"]
    assert provider.calls >= 2


@pytest.mark.asyncio
async def test_rpc_steering_queue_modes(tmp_path):
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    provider = PlainProvider()
    session.provider_registry._providers["openai"] = provider

    rpc = RpcMode(session)
    output = []
    rpc._write = lambda payload: output.append(payload)

    await rpc._handle({"type": "set_steering_mode", "mode": "one-at-a-time"})
    assert output[-1]["command"] == "set_steering_mode"
    assert output[-1]["success"] is True
    await rpc._handle({"type": "steer", "message": "a"})
    await rpc._handle({"type": "steer", "message": "b"})
    await rpc._handle({"type": "get_state"})
    assert output[-1]["data"]["steeringQueueCount"] == 2
    await rpc._handle({"type": "continue"})
    await rpc._handle({"type": "get_state"})
    assert output[-1]["data"]["steeringQueueCount"] == 0

    await rpc._handle({"type": "set_steering_mode", "mode": "all"})
    assert output[-1]["command"] == "set_steering_mode"
    assert output[-1]["success"] is True


@pytest.mark.asyncio
async def test_rpc_follow_up_queue_mode_affects_turn_count(tmp_path):
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    provider = PlainProvider()
    session.provider_registry._providers["openai"] = provider

    rpc = RpcMode(session)
    rpc._write = lambda _payload: None

    await rpc._handle({"type": "set_follow_up_mode", "mode": "one-at-a-time"})
    await rpc._handle({"type": "follow_up", "message": "f1"})
    await rpc._handle({"type": "follow_up", "message": "f2"})
    await rpc._handle({"type": "continue"})
    calls_one_at_a_time = provider.calls

    await rpc._handle({"type": "new_session"})
    await rpc._handle({"type": "set_follow_up_mode", "mode": "all"})
    await rpc._handle({"type": "follow_up", "message": "f1"})
    await rpc._handle({"type": "follow_up", "message": "f2"})
    await rpc._handle({"type": "continue"})
    calls_all = provider.calls - calls_one_at_a_time

    assert calls_one_at_a_time == 3
    assert calls_all == 2


@pytest.mark.asyncio
async def test_rpc_abort_cancels_inflight_prompt(tmp_path):
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    provider = SlowProvider()
    session.provider_registry._providers["openai"] = provider

    rpc = RpcMode(session)
    output = []
    rpc._write = lambda payload: output.append(payload)

    prompt_task = asyncio.create_task(rpc._handle({"type": "prompt", "id": "p1", "message": "hello"}))
    await asyncio.sleep(0.05)
    await rpc._handle({"type": "abort", "id": "a1"})
    await asyncio.wait_for(prompt_task, timeout=2)

    abort_response = next(item for item in output if item.get("command") == "abort")
    prompt_response = next(item for item in output if item.get("command") == "prompt")
    assert abort_response["success"] is True
    assert prompt_response["success"] is True

    last_assistant = next((m for m in reversed(session.get_messages()) if getattr(m, "role", "") == "assistant"), None)
    assert last_assistant is not None
    assert last_assistant.stop_reason == "aborted"
    assert last_assistant.error_message == "Request was aborted"
    assert provider.calls == 1


@pytest.mark.asyncio
async def test_rpc_run_nonblocking_stdin_allows_prompt_response(tmp_path, monkeypatch):
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    provider = PlainProvider()
    session.provider_registry._providers["openai"] = provider

    rpc = RpcMode(session)
    output = []
    rpc._write = lambda payload: output.append(payload)

    fake_stdin = _BlockingStdin(json.dumps({"type": "prompt", "id": "p1", "message": "hello"}, ensure_ascii=False))
    monkeypatch.setattr("gen_agent.modes.rpc_mode.sys.stdin", fake_stdin)

    run_task = asyncio.create_task(rpc.run())
    try:
        for _ in range(60):
            if any(
                item.get("type") == "response" and item.get("command") == "prompt" and item.get("id") == "p1"
                for item in output
            ):
                break
            await asyncio.sleep(0.05)
        else:
            raise AssertionError("Did not receive prompt response while waiting for stdin")
    finally:
        fake_stdin.release()

    code = await asyncio.wait_for(run_task, timeout=2)
    assert code == 0
    assert provider.calls == 1
