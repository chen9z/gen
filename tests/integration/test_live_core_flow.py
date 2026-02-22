from __future__ import annotations

import json
import os
import select
import shlex
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest


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

    enabled = _read_first_config_var(
        ["RUN_PROVIDER_TESTS", "RUN_LIVE_PROVIDER_TESTS"],
        dotenv_values,
    ).lower()
    if enabled not in {"1", "true", "yes", "on"}:
        pytest.skip(
            "live tests disabled. Set RUN_PROVIDER_TESTS=1 in env or .env to enable."
        )

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


def _tool_prompt(probe_file: Path) -> str:
    return (
        f"必须先调用 read 工具读取文件 {probe_file}，"
        "然后只输出文件中的字符串本身，不要任何额外字符。"
    )


def _run_cmd(args: list[str], timeout_sec: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout_sec, check=False)


@pytest.mark.live
def test_live_core_flow_print_json_rpc_with_tool_calls(tmp_path: Path) -> None:
    cfg = _load_live_config()

    nonce = f"TOOL_NONCE_{uuid.uuid4().hex.upper()}"
    probe_file = tmp_path / "tool_probe.txt"
    probe_file.write_text(f"{nonce}\n", encoding="utf-8")
    prompt = _tool_prompt(probe_file)

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
        "--no-session",
        "--cwd",
        str(Path.cwd()),
    ]

    # print mode: strict nonce equality (with trim)
    print_proc = _run_cmd([*base_args, "--mode", "print", prompt])
    assert print_proc.returncode == 0, print_proc.stderr or print_proc.stdout
    print_actual = (print_proc.stdout or "").strip().splitlines()[-1].strip()
    assert print_actual == nonce

    # json mode: must have tool events + agent_end + final assistant text equals nonce
    json_proc = _run_cmd([*base_args, "--mode", "json", prompt])
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

    json_assistant_text = ""
    for row in rows:
        message = row.get("message")
        if isinstance(message, dict) and message.get("role") == "assistant":
            for block in message.get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    text = (block.get("text") or "").strip()
                    if text:
                        json_assistant_text = text
    assert json_assistant_text == nonce

    # rpc mode: interactive stdin, validate responses + tool events + get_messages content
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
    send({"type": "prompt", "id": "p1", "message": prompt})

    seen_objs: list[dict] = []
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
    assert any(isinstance(message, dict) and message.get("role") == "toolResult" for message in messages)

    rpc_assistant_text = ""
    for message in messages:
        if isinstance(message, dict) and message.get("role") == "assistant":
            for block in message.get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    text = (block.get("text") or "").strip()
                    if text:
                        rpc_assistant_text = text
    assert rpc_assistant_text == nonce
