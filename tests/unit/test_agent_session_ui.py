from __future__ import annotations

from gen_agent.extensions import NoOpExtensionUIContext
from gen_agent.runtime import SessionRuntime


def test_bind_ui_context_respects_ui_extensions_setting(tmp_path) -> None:
    session = SessionRuntime(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    custom = NoOpExtensionUIContext()

    session.settings.ui_extensions_enabled = False
    session.bind_ui_context(custom)
    assert session.ui is not custom

    session.settings.ui_extensions_enabled = True
    session.bind_ui_context(custom)
    assert session.ui is custom
