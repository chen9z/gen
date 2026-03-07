from __future__ import annotations

import json
from pathlib import Path

import pytest

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage
from gen_agent.runtime import SessionRuntime


class _CaptureProvider:
    def __init__(self) -> None:
        self.last_request = None

    async def complete(self, request):
        self.last_request = request
        return AssistantMessage(
            provider=request.provider,
            model=request.model_id,
            content=[TextContent(text="ok")],
        )


@pytest.mark.asyncio
async def test_agent_session_provider_call_uses_registry_runtime_model_config(tmp_path: Path, monkeypatch) -> None:
    xdg = tmp_path / "xdg"
    model_file = xdg / "gen-agent" / "models.json"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(
        json.dumps(
            {
                "providers": {
                    "anthropic": {
                        "baseUrl": "https://anthropic-proxy.local/v1",
                        "apiKey": "MODEL_ANTHROPIC_KEY",
                        "headers": {
                            "x-api-version": "ANTHROPIC_VERSION",
                            "x-from-models": "literal-header",
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))
    monkeypatch.setenv("ANTHROPIC_VERSION", "2024-01-01")

    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="anthropic",
        model="claude-3-5-sonnet-latest",
        persist_session=False,
    )
    capture_provider = _CaptureProvider()
    session.provider_registry._providers["anthropic"] = capture_provider

    messages = await session.prompt("hello")

    assert messages
    assert capture_provider.last_request is not None
    request = capture_provider.last_request
    assert request.provider == "anthropic"
    assert request.model_id == "claude-3-5-sonnet-latest"
    assert request.api_key == "MODEL_ANTHROPIC_KEY"
    assert request.base_url == "https://anthropic-proxy.local/v1"
    assert request.headers == {
        "x-api-version": "2024-01-01",
        "x-from-models": "literal-header",
    }
