from __future__ import annotations

import json
import os
import select
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import pytest
from gen_agent.tools.registry import create_all_tools


@dataclass
class LiveConfig:
    provider: str
    model: str
    base_url: str
    api_key: str


def _load_dotenv_values(dotenv_path: Path) -> dict[str, str]:
    if not dotenv_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            continue
        if value and (value[0] == value[-1]) and value[0] in {"'", '"'}:
            value = value[1:-1]
        else:
            # Keep parser simple: support inline comments only for unquoted values.
            if " #" in value:
                value = value.split(" #", 1)[0].rstrip()
            if value.startswith(('"', "'")):
                try:
                    value = shlex.split(value)[0]
                except Exception:
                    pass
        values[key] = value
    return values


def _read_config_var(name: str, dotenv_values: dict[str, str], default: str = "") -> str:
    # Shell environment has priority over .env file values.
    current = os.environ.get(name)
    if current is not None and current.strip():
        return current.strip()
    return dotenv_values.get(name, default).strip()


def _read_first_config_var(names: list[str], dotenv_values: dict[str, str], default: str = "") -> str:
    for name in names:
        value = _read_config_var(name, dotenv_values)
        if value:
            return value
    return default


def _load_live_config() -> LiveConfig:
    default_dotenv = Path(__file__).resolve().parents[2] / ".env"
    dotenv_path = Path(
        (os.environ.get("LIVE_DOTENV_PATH") or str(default_dotenv)).strip()
    ).expanduser()
    dotenv_values = _load_dotenv_values(dotenv_path)

    provider = _read_first_config_var(["PROVIDER", "LIVE_PROVIDER"], dotenv_values, "anthropic")
    model = _read_first_config_var(["MODEL", "LIVE_MODEL"], dotenv_values)
    base_url = _read_first_config_var(["BASE_URL", "LIVE_BASE_URL"], dotenv_values)
    api_key = _read_first_config_var(
        ["API_KEY", "LIVE_API_KEY", "MINIMAX_API_KEY"],
        dotenv_values,
    )

    missing = [
        name
        for name, value in [
            ("MODEL", model),
            ("BASE_URL", base_url),
            ("API_KEY", api_key),
        ]
        if not value
    ]
    if missing:
        pytest.skip(f"live tests missing required env vars: {', '.join(missing)}")

    return LiveConfig(provider=provider, model=model, base_url=base_url, api_key=api_key)


def _tools_round1_prompt() -> str:
    return (
        "当前项目使用了哪些 tools？\n"
        "请先调用 read 工具读取 src/gen_agent/tools/registry.py，"
        "从 create_all_tools 中提取工具名。\n"
        "最终只输出两行（不要输出任何其它内容）：\n"
        "KW_TOOLS_COUNT=<工具数量>\n"
        "KW_TOOLS_LIST=<按字母排序、逗号分隔的工具名>"
    )


def _tools_round2_prompt() -> str:
    return (
        "请基于上一轮结果做多轮确认，不要输出解释。\n"
        "只输出三行：\n"
        "KW_MULTI_TURN_OK=1\n"
        "KW_TOOLS_COUNT=<与上一轮一致>\n"
        "KW_TOOLS_LIST=<与上一轮一致>"
    )


def _run_cmd(args: list[str], timeout_sec: int = 240) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout_sec, check=False)


def _extract_assistant_text(message: dict | None) -> str:
    if not isinstance(message, dict) or message.get("role") != "assistant":
        return ""
    parts: list[str] = []
    for block in message.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            text = (block.get("text") or "").strip()
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def _parse_keywords(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("KW_") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def _assert_keywords(text: str, expected_tools: list[str], require_multi_turn: bool = False) -> dict[str, str]:
    data = _parse_keywords(text)
    assert data.get("KW_TOOLS_COUNT") == str(len(expected_tools)), text
    actual_list_raw = data.get("KW_TOOLS_LIST", "")
    actual_tools = [item.strip() for item in actual_list_raw.split(",") if item.strip()]
    assert actual_tools == expected_tools, text
    if require_multi_turn:
        assert data.get("KW_MULTI_TURN_OK") == "1", text
    return data


@pytest.mark.live
def test_live_core_flow_print_json_rpc_with_tool_calls(tmp_path: Path) -> None:
    cfg = _load_live_config()
    expected_tools = sorted(create_all_tools(str(Path.cwd())).keys())
    tools_csv = ",".join(expected_tools)
    round1_prompt = _tools_round1_prompt()
    round2_prompt = _tools_round2_prompt()

    base_args = [
        "uv",
        "run",
        "gen",
        "--provider",
        cfg.provider,
        "--model",
        cfg.model,
        "--base-url",
        cfg.base_url,
        "--api-key",
        cfg.api_key,
        "--thinking",
        "high",
        "--tools",
        tools_csv,
        "--no-session",
        "--cwd",
        str(Path.cwd()),
    ]

    # print mode: validate keyword output
    print_proc = _run_cmd([*base_args, "--mode", "print", round1_prompt])
    assert print_proc.returncode == 0, print_proc.stderr or print_proc.stdout
    _assert_keywords(print_proc.stdout or "", expected_tools)

    # json mode: validate tool events + keyword output
    json_proc = _run_cmd([*base_args, "--mode", "json", round1_prompt])
    assert json_proc.returncode == 0, json_proc.stderr or json_proc.stdout
    rows = [
        json.loads(line)
        for line in (json_proc.stdout or "").splitlines()
        if line.strip().startswith("{")
    ]
    has_tool_start = any(row.get("type") == "tool_execution_start" for row in rows)
    has_tool_end = any(row.get("type") == "tool_execution_end" for row in rows)
    has_agent_end = any(row.get("type") == "agent_end" for row in rows)
    assert has_tool_start and has_tool_end and has_agent_end
    json_tool_names = {
        (row.get("toolName") or "").strip()
        for row in rows
        if row.get("type") == "tool_execution_start"
    }
    assert "read" in json_tool_names

    json_assistant_text = ""
    for row in rows:
        text = _extract_assistant_text(row.get("message"))
        if text:
            json_assistant_text = text
    _assert_keywords(json_assistant_text, expected_tools)

    # rpc mode: two rounds, validate multi-turn + tool events + keyword output
    rpc_cmd = [*base_args, "--mode", "rpc"]
    proc = subprocess.Popen(
        rpc_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdin is not None
    assert proc.stdout is not None

    def send(payload: dict) -> None:
        proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        proc.stdin.flush()

    send({"type": "set_thinking_level", "id": "th1", "level": "high"})
    send({"type": "prompt", "id": "p1", "message": round1_prompt})

    seen_objs: list[dict] = []
    sent_p2 = False
    sent_m1 = False
    deadline = time.time() + 240
    while time.time() < deadline:
        ready, _, _ = select.select([proc.stdout], [], [], 1.0)
        if not ready:
            if proc.poll() is not None:
                break
            continue
        line = proc.stdout.readline()
        if not line:
            if proc.poll() is not None:
                break
            continue
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
        except Exception:
            continue
        seen_objs.append(obj)

        if (
            obj.get("type") == "response"
            and obj.get("id") == "p1"
            and obj.get("command") == "prompt"
            and obj.get("success") is True
            and not sent_p2
        ):
            send({"type": "prompt", "id": "p2", "message": round2_prompt})
            sent_p2 = True

        if (
            obj.get("type") == "response"
            and obj.get("id") == "p2"
            and obj.get("command") == "prompt"
            and obj.get("success") is True
            and not sent_m1
        ):
            send({"type": "get_messages", "id": "m1"})
            sent_m1 = True

        if obj.get("type") == "response" and obj.get("id") == "m1" and obj.get("command") == "get_messages":
            break

    try:
        proc.stdin.close()
    except Exception:
        pass
    try:
        proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=8)

    need = {
        ("th1", "set_thinking_level"),
        ("p1", "prompt"),
        ("p2", "prompt"),
        ("m1", "get_messages"),
    }
    seen_responses = {
        (obj.get("id"), obj.get("command"))
        for obj in seen_objs
        if obj.get("type") == "response" and obj.get("success") is True
    }
    assert not (need - seen_responses), {"missing_responses": sorted(need - seen_responses)}

    rpc_has_tool_start = any(obj.get("type") == "tool_execution_start" for obj in seen_objs)
    rpc_has_tool_end = any(obj.get("type") == "tool_execution_end" for obj in seen_objs)
    assert rpc_has_tool_start and rpc_has_tool_end
    rpc_turn_end_count = sum(1 for obj in seen_objs if obj.get("type") == "turn_end")
    assert rpc_turn_end_count >= 2

    m1 = next(
        (
            obj
            for obj in seen_objs
            if obj.get("type") == "response" and obj.get("id") == "m1" and obj.get("command") == "get_messages"
        ),
        None,
    )
    assert m1 is not None
    messages = ((m1.get("data") or {}).get("messages") or [])
    assert any(isinstance(msg, dict) and msg.get("role") == "toolResult" for msg in messages)

    assistant_texts = [
        _extract_assistant_text(msg)
        for msg in messages
        if isinstance(msg, dict) and msg.get("role") == "assistant"
    ]
    assistant_texts = [text for text in assistant_texts if text]
    assert len(assistant_texts) >= 2
    _assert_keywords(assistant_texts[-2], expected_tools)
    _assert_keywords(assistant_texts[-1], expected_tools, require_multi_turn=True)
