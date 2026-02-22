from gen_agent.core.session_manager import migrate_rows
from gen_agent.core.session_manager import SessionManager


def test_migrate_v1_to_v3() -> None:
    rows = [
        {"type": "session", "id": "s", "timestamp": "2026-01-01T00:00:00Z", "cwd": "/tmp"},
        {
            "type": "message",
            "timestamp": "2026-01-01T00:00:01Z",
            "message": {"role": "hookMessage", "customType": "x", "content": "y", "display": True, "timestamp": 1},
        },
    ]

    migrated, changed = migrate_rows(rows)
    assert changed is True
    assert migrated[0]["version"] == 3
    assert migrated[1]["id"]
    assert migrated[1]["parentId"] is None
    assert migrated[1]["message"]["role"] == "custom"


def test_migrate_compaction_first_kept_index_header_relative() -> None:
    rows = [
        {"type": "session", "id": "s", "timestamp": "2026-01-01T00:00:00Z", "cwd": "/tmp"},
        {"type": "message", "id": "m1", "timestamp": "2026-01-01T00:00:01Z", "message": {"role": "user", "content": "a", "timestamp": 1}},
        {"type": "message", "id": "m2", "timestamp": "2026-01-01T00:00:02Z", "message": {"role": "assistant", "content": [{"type": "text", "text": "b"}], "timestamp": 2}},
        {"type": "compaction", "id": "c1", "timestamp": "2026-01-01T00:00:03Z", "firstKeptEntryIndex": 1, "summary": "s", "tokensBefore": 10},
    ]

    migrated, changed = migrate_rows(rows)
    assert changed is True
    compaction = migrated[3]
    assert compaction.get("firstKeptEntryId") == "m1"


def test_migrate_compaction_first_kept_index_entry_relative() -> None:
    rows = [
        {"type": "session", "id": "s", "timestamp": "2026-01-01T00:00:00Z", "cwd": "/tmp"},
        {"type": "message", "id": "m1", "timestamp": "2026-01-01T00:00:01Z", "message": {"role": "user", "content": "a", "timestamp": 1}},
        {"type": "message", "id": "m2", "timestamp": "2026-01-01T00:00:02Z", "message": {"role": "assistant", "content": [{"type": "text", "text": "b"}], "timestamp": 2}},
        {"type": "compaction", "id": "c1", "timestamp": "2026-01-01T00:00:03Z", "firstKeptEntryIndex": 0, "summary": "s", "tokensBefore": 10},
    ]

    migrated, changed = migrate_rows(rows)
    assert changed is True
    compaction = migrated[3]
    assert compaction.get("firstKeptEntryId") == "m1"


def test_load_or_set_file_uses_requested_path(tmp_path) -> None:
    session_dir = tmp_path / "sessions"
    manager = SessionManager(cwd=str(tmp_path), persist=True, session_dir=str(session_dir))
    target = (session_dir / "explicit.jsonl").resolve()

    manager.load_or_set_file(str(target))

    assert manager.file == target
    assert target.exists()
    assert manager.entries == []
