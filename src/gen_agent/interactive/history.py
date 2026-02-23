from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import md5
from pathlib import Path

from gen_agent.core.paths import global_root


@dataclass(slots=True)
class HistoryEntry:
    content: str


class HistoryStore:
    def __init__(self, cwd: str) -> None:
        self.cwd = cwd
        self.path = self._history_path(cwd)
        self._last_content: str | None = None

    @staticmethod
    def _history_path(cwd: str) -> Path:
        work_dir_id = md5(cwd.encode("utf-8")).hexdigest()
        return global_root() / "user-history" / f"{work_dir_id}.jsonl"

    def load(self) -> list[str]:
        if not self.path.exists():
            return []
        entries: list[str] = []
        try:
            for raw_line in self.path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                content = payload.get("content") if isinstance(payload, dict) else None
                if not isinstance(content, str):
                    continue
                text = content.strip()
                if not text:
                    continue
                entries.append(text)
        except OSError:
            return entries
        if entries:
            self._last_content = entries[-1]
        return entries

    def append(self, content: str) -> None:
        text = content.strip()
        if not text:
            return
        if text == self._last_content:
            return
        record = HistoryEntry(content=text)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
            self._last_content = text
        except OSError:
            return
