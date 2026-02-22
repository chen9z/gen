from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from gen_agent.models.messages import (
    AgentMessage,
    BranchSummaryMessage,
    CompactionSummaryMessage,
    CustomMessage,
)
from gen_agent.models.session import (
    CURRENT_SESSION_VERSION,
    BranchSummaryEntry,
    CompactionEntry,
    FileEntry,
    SessionEntry,
    SessionHeader,
    SessionInfoEntry,
    SessionMessageEntry,
)

from .paths import ensure_dir, session_dir_for_cwd


def _id8() -> str:
    return uuid.uuid4().hex[:8]


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


_file_entry_adapter = TypeAdapter(FileEntry)
_session_entry_adapter = TypeAdapter(SessionEntry)


@dataclass
class SessionContext:
    messages: list[AgentMessage]
    thinking_level: str
    model: dict[str, str] | None


@dataclass
class SessionSummary:
    path: str
    modified: float
    message_count: int
    first_user_message: str
    session_name: str | None


def _parse_entries(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def migrate_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], bool]:
    if not rows:
        return rows, False
    changed = False
    header = rows[0]
    version = int(header.get("version", 1))

    if version < 2:
        prev_id: str | None = None
        for row in rows[1:]:
            row.setdefault("id", _id8())
            row.setdefault("parentId", prev_id)
            prev_id = row["id"]
            if row.get("type") == "compaction" and "firstKeptEntryIndex" in row:
                idx = row.pop("firstKeptEntryIndex")
                if isinstance(idx, int):
                    candidates = []
                    if 0 <= idx < len(rows):
                        candidates.append(rows[idx])
                    # Some historical writers stored index relative to entries (excluding header).
                    if 0 <= idx + 1 < len(rows):
                        candidates.append(rows[idx + 1])
                    for target in candidates:
                        if target.get("type") == "session":
                            continue
                        target_id = target.get("id")
                        if target_id:
                            row["firstKeptEntryId"] = target_id
                            break
        header["version"] = 2
        changed = True

    if version < 3:
        for row in rows[1:]:
            if row.get("type") == "message":
                msg = row.get("message") or {}
                if msg.get("role") == "hookMessage":
                    msg["role"] = "custom"
        header["version"] = 3
        changed = True

    return rows, changed


class SessionManager:
    def __init__(
        self,
        cwd: str,
        persist: bool = True,
        session_dir: str | None = None,
        session_file: str | None = None,
    ):
        self.cwd = str(Path(cwd).resolve())
        self.persist = persist
        self.session_dir = Path(session_dir) if session_dir else session_dir_for_cwd(self.cwd)
        self.file: Path | None = Path(session_file).resolve() if session_file else None
        self.header: SessionHeader | None = None
        self.entries: list[SessionEntry] = []
        self.by_id: dict[str, SessionEntry] = {}
        self.leaf_id: str | None = None

        if self.file and self.file.exists():
            self._load(self.file)
        else:
            self.new_session()

    def _reindex(self) -> None:
        self.by_id = {entry.id: entry for entry in self.entries}
        self.leaf_id = self.entries[-1].id if self.entries else None

    def _append_raw(self, row: dict[str, Any]) -> None:
        if not self.persist or not self.file:
            return
        ensure_dir(self.file.parent)
        with self.file.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False))
            fh.write("\n")

    def _rewrite_file(self) -> None:
        if not self.persist or not self.file or not self.header:
            return
        ensure_dir(self.file.parent)
        rows: list[dict[str, Any]] = [self.header.model_dump(by_alias=True, exclude_none=True)]
        rows.extend(entry.model_dump(by_alias=True, exclude_none=True) for entry in self.entries)
        with self.file.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False))
                fh.write("\n")

    def _load(self, path: Path) -> None:
        rows = _parse_entries(path.read_text(encoding="utf-8"))
        rows, migrated = migrate_rows(rows)
        if not rows:
            self.new_session()
            return

        self.header = SessionHeader.model_validate(rows[0])
        self.entries = []
        for row in rows[1:]:
            try:
                self.entries.append(_session_entry_adapter.validate_python(row))
            except Exception:
                continue
        self.file = path
        self._reindex()

        if migrated:
            self._rewrite_file()

    def new_session(self, parent_session: str | None = None) -> Path | None:
        sid = str(uuid.uuid4())
        ts = _utcnow_iso()
        self.header = SessionHeader(
            id=sid,
            timestamp=ts,
            cwd=self.cwd,
            parentSession=parent_session,
            version=CURRENT_SESSION_VERSION,
        )
        self.entries = []
        self.by_id = {}
        self.leaf_id = None
        if self.persist:
            ensure_dir(self.session_dir)
            self.file = self.session_dir / f"{ts.replace(':', '-').replace('.', '-')}_{sid}.jsonl"
            self._rewrite_file()
        return self.file

    def append_entry(self, entry: SessionEntry) -> None:
        self.entries.append(entry)
        self.by_id[entry.id] = entry
        self.leaf_id = entry.id
        self._append_raw(entry.model_dump(by_alias=True, exclude_none=True))

    def append_message(self, message: AgentMessage) -> SessionMessageEntry:
        entry = SessionMessageEntry(
            id=_id8(),
            parentId=self.leaf_id,
            timestamp=_utcnow_iso(),
            message=message,
        )
        self.append_entry(entry)
        return entry

    def append_model_change(self, provider: str, model_id: str) -> None:
        from gen_agent.models.session import ModelChangeEntry

        self.append_entry(
            ModelChangeEntry(
                id=_id8(),
                parentId=self.leaf_id,
                timestamp=_utcnow_iso(),
                provider=provider,
                modelId=model_id,
            )
        )

    def append_thinking_level(self, level: str) -> None:
        from gen_agent.models.session import ThinkingLevelChangeEntry

        self.append_entry(
            ThinkingLevelChangeEntry(
                id=_id8(),
                parentId=self.leaf_id,
                timestamp=_utcnow_iso(),
                thinkingLevel=level,
            )
        )

    def append_compaction(self, summary: str, first_kept_entry_id: str, tokens_before: int) -> CompactionEntry:
        entry = CompactionEntry(
            id=_id8(),
            parentId=self.leaf_id,
            timestamp=_utcnow_iso(),
            summary=summary,
            firstKeptEntryId=first_kept_entry_id,
            tokensBefore=tokens_before,
        )
        self.append_entry(entry)
        return entry

    def append_branch_summary(self, summary: str, from_id: str) -> BranchSummaryEntry:
        entry = BranchSummaryEntry(
            id=_id8(),
            parentId=self.leaf_id,
            timestamp=_utcnow_iso(),
            summary=summary,
            fromId=from_id,
        )
        self.append_entry(entry)
        return entry

    def set_session_name(self, name: str) -> None:
        entry = SessionInfoEntry(
            id=_id8(),
            parentId=self.leaf_id,
            timestamp=_utcnow_iso(),
            name=name,
        )
        self.append_entry(entry)

    def get_session_name(self) -> str | None:
        for entry in reversed(self.entries):
            if isinstance(entry, SessionInfoEntry) and entry.name:
                return entry.name
        return None

    def get_branch(self, leaf_id: str | None = None) -> list[SessionEntry]:
        if not self.entries:
            return []
        leaf = leaf_id if leaf_id is not None else self.leaf_id
        if leaf is None:
            return []
        out: list[SessionEntry] = []
        current = self.by_id.get(leaf)
        while current is not None:
            out.append(current)
            if current.parent_id is None:
                break
            current = self.by_id.get(current.parent_id)
        out.reverse()
        return out

    def build_context(self, leaf_id: str | None = None) -> SessionContext:
        branch = self.get_branch(leaf_id)
        messages: list[AgentMessage] = []
        thinking_level = "off"
        model: dict[str, str] | None = None

        compaction: CompactionEntry | None = None
        for entry in branch:
            if entry.type == "thinking_level_change":
                thinking_level = getattr(entry, "thinking_level", "off")
            elif entry.type == "model_change":
                model = {"provider": getattr(entry, "provider"), "modelId": getattr(entry, "model_id")}
            elif entry.type == "message":
                message_entry = entry
                if getattr(message_entry.message, "role", "") == "assistant":
                    provider = getattr(message_entry.message, "provider", "")
                    model_id = getattr(message_entry.message, "model", "")
                    if provider and model_id and provider != "system" and model_id != "gen":
                        model = {
                            "provider": provider,
                            "modelId": model_id,
                        }
            elif entry.type == "compaction":
                compaction = entry

        if compaction:
            messages.append(
                CompactionSummaryMessage(
                    summary=compaction.summary,
                    tokensBefore=compaction.tokens_before,
                    timestamp=__import__("time").time_ns() // 1_000_000,
                )
            )
            start_collecting = False
            appended_message_entry_ids: set[str] = set()
            for entry in branch:
                if entry.id == compaction.first_kept_entry_id:
                    start_collecting = True
                if start_collecting and entry.type == "message":
                    messages.append(entry.message)
                    appended_message_entry_ids.add(entry.id)
            for entry in branch:
                if entry.id == compaction.id:
                    continue
                if entry.parent_id == compaction.id and entry.type == "message":
                    if entry.id in appended_message_entry_ids:
                        continue
                    messages.append(entry.message)
        else:
            for entry in branch:
                if entry.type == "message":
                    messages.append(entry.message)
                elif entry.type == "branch_summary":
                    messages.append(
                        BranchSummaryMessage(
                            summary=entry.summary,
                            fromId=entry.from_id,
                            timestamp=__import__("time").time_ns() // 1_000_000,
                        )
                    )
                elif entry.type == "custom":
                    messages.append(
                        CustomMessage(
                            customType=getattr(entry, "custom_type", "custom"),
                            content=str(getattr(entry, "data", "")),
                            display=True,
                            timestamp=__import__("time").time_ns() // 1_000_000,
                        )
                    )

        return SessionContext(messages=messages, thinking_level=thinking_level, model=model)

    def load_or_set_file(self, path: str) -> None:
        self.file = Path(path).resolve()
        if self.file.exists():
            self._load(self.file)
        else:
            sid = str(uuid.uuid4())
            ts = _utcnow_iso()
            self.header = SessionHeader(
                id=sid,
                timestamp=ts,
                cwd=self.cwd,
                parentSession=None,
                version=CURRENT_SESSION_VERSION,
            )
            self.entries = []
            self.by_id = {}
            self.leaf_id = None
            if self.file:
                self._rewrite_file()

    def set_leaf(self, leaf_id: str | None) -> bool:
        if leaf_id is None:
            self.leaf_id = None
            return True
        if leaf_id not in self.by_id:
            return False
        self.leaf_id = leaf_id
        return True

    def get_tree_entries(self) -> list[dict[str, Any]]:
        return [
            {
                "id": entry.id,
                "parentId": entry.parent_id,
                "type": entry.type,
                "timestamp": entry.timestamp,
            }
            for entry in self.entries
        ]

    def get_latest_session_files(self, limit: int = 20) -> list[Path]:
        if not self.session_dir.exists():
            return []
        files = [p for p in self.session_dir.glob("*.jsonl") if p.is_file()]
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return files[:limit]

    def list_sessions(self, limit: int = 20) -> list[SessionSummary]:
        out: list[SessionSummary] = []
        for file in self.get_latest_session_files(limit=limit):
            try:
                rows = _parse_entries(file.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not rows or rows[0].get("type") != "session":
                continue

            message_count = 0
            first_user_message = ""
            session_name: str | None = None
            for row in rows[1:]:
                if row.get("type") == "session_info" and row.get("name"):
                    session_name = str(row.get("name"))
                if row.get("type") != "message":
                    continue
                message_count += 1
                message = row.get("message") or {}
                if not first_user_message and message.get("role") == "user":
                    content = message.get("content")
                    if isinstance(content, str):
                        first_user_message = content
                    elif isinstance(content, list):
                        texts = [block.get("text", "") for block in content if block.get("type") == "text"]
                        first_user_message = " ".join(texts)

            out.append(
                SessionSummary(
                    path=str(file),
                    modified=file.stat().st_mtime,
                    message_count=message_count,
                    first_user_message=first_user_message[:120],
                    session_name=session_name,
                )
            )
        return out

    def switch_session_file(self, path: str) -> None:
        self.load_or_set_file(path)

    def fork_current_branch(self, leaf_id: str | None = None) -> Path | None:
        current_file = str(self.file) if self.file else None
        branch = self.get_branch(leaf_id)

        self.new_session(parent_session=current_file)
        self.entries = []
        self.by_id = {}
        self.leaf_id = None
        self._rewrite_file()

        for entry in branch:
            self.append_entry(entry)
        return self.file
