from __future__ import annotations

from pathlib import Path

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.messages import UserMessage


def test_list_sessions_supports_offset_and_include_current(tmp_path: Path) -> None:
    session_dir = tmp_path / "sessions"
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        session_dir=str(session_dir),
    )

    session.session_manager.append_message(UserMessage(content="s1"))
    first_path = session.session_file

    session.new_session()
    session.session_manager.append_message(UserMessage(content="s2"))
    second_path = session.session_file

    session.new_session()
    session.session_manager.append_message(UserMessage(content="s3"))
    third_path = session.session_file

    assert third_path and second_path and first_path

    without_current = session.list_sessions(limit=2, include_current=False)
    assert without_current
    assert all(item["path"] != third_path for item in without_current)

    offset_one = session.list_sessions(limit=1, offset=1, include_current=False)
    assert len(offset_one) == 1
    assert offset_one[0]["path"] in {first_path, second_path}


def test_get_tree_supports_limit_and_include_root(tmp_path: Path) -> None:
    session = AgentSession(
        cwd=str(tmp_path),
        provider="openai",
        model="gpt-4o-mini",
        api_key="x",
        persist_session=False,
    )
    session.session_manager.append_message(UserMessage(content="a"))
    session.session_manager.append_message(UserMessage(content="b"))

    tree = session.get_tree(limit=1, include_root=True)
    entries = tree["entries"]
    assert len(entries) == 2
    assert entries[0]["id"] is None
    assert entries[0]["type"] == "root"
    assert entries[1]["type"] == "message"
