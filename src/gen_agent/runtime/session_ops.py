from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from gen_agent.core.compaction import generate_compaction_summary

if TYPE_CHECKING:
    from gen_agent.core.session_manager import SessionManager
    from gen_agent.runtime.model_controller import ModelController


class SessionOps:
    def __init__(
        self,
        *,
        session_manager: "SessionManager",
        model_controller: "ModelController",
        auto_compaction_enabled_getter: Callable[[], bool],
        steering_mode_getter: Callable[[], str],
        follow_up_mode_getter: Callable[[], str],
        tools_getter: Callable[[], list[str]],
        extension_flags_getter: Callable[[], dict[str, bool | str]],
        steering_queue_count_getter: Callable[[], int],
        follow_up_queue_count_getter: Callable[[], int],
    ) -> None:
        self._session_manager = session_manager
        self._model_controller = model_controller
        self._auto_compaction_enabled_getter = auto_compaction_enabled_getter
        self._steering_mode_getter = steering_mode_getter
        self._follow_up_mode_getter = follow_up_mode_getter
        self._tools_getter = tools_getter
        self._extension_flags_getter = extension_flags_getter
        self._steering_queue_count_getter = steering_queue_count_getter
        self._follow_up_queue_count_getter = follow_up_queue_count_getter

    def get_messages(self):
        return self._session_manager.build_context().messages

    def get_state(self) -> dict[str, Any]:
        header = self._session_manager.header
        steering_count = self._steering_queue_count_getter()
        follow_up_count = self._follow_up_queue_count_getter()
        return {
            "provider": self._model_controller.provider_name,
            "modelId": self._model_controller.model_id,
            "thinkingLevel": self._model_controller.thinking_level,
            "isStreaming": False,
            "isCompacting": False,
            "steeringMode": self._steering_mode_getter(),
            "followUpMode": self._follow_up_mode_getter(),
            "sessionFile": str(self._session_manager.file) if self._session_manager.file else None,
            "sessionId": header.id if header else None,
            "sessionName": self._session_manager.get_session_name(),
            "autoCompactionEnabled": self._auto_compaction_enabled_getter(),
            "messageCount": len(self._session_manager.build_context().messages),
            "pendingMessageCount": steering_count + follow_up_count,
            "steeringQueueCount": steering_count,
            "followUpQueueCount": follow_up_count,
            "tools": self._tools_getter(),
            "extensionFlags": dict(self._extension_flags_getter()),
        }

    def list_sessions(self, limit: int = 20, offset: int = 0, include_current: bool = True) -> list[dict[str, Any]]:
        safe_limit = max(1, limit)
        safe_offset = max(0, offset)
        requested = safe_limit + safe_offset + (1 if not include_current else 0)
        sessions = [
            {
                "path": item.path,
                "modified": item.modified,
                "messageCount": item.message_count,
                "firstMessage": item.first_user_message,
                "name": item.session_name,
            }
            for item in self._session_manager.list_sessions(limit=requested)
        ]
        if not include_current:
            current = str(self._session_manager.file) if self._session_manager.file else None
            sessions = [row for row in sessions if row["path"] != current]
        if safe_offset:
            sessions = sessions[safe_offset:]
        return sessions[:safe_limit]

    def get_tree(self, limit: int | None = None, include_root: bool = False) -> dict[str, Any]:
        entries = self._session_manager.get_tree_entries()
        if limit is not None:
            entries = entries[-max(1, limit) :]
        if include_root:
            entries = [{"id": None, "parentId": None, "type": "root", "timestamp": None}, *entries]
        return {"leafId": self._session_manager.leaf_id, "entries": entries}

    def switch_tree(self, leaf_id: str | None) -> bool:
        return self._session_manager.set_leaf(leaf_id)

    def resume_session(self, target: str | int) -> str:
        if isinstance(target, int):
            sessions = self._session_manager.list_sessions(limit=50)
            index = target - 1
            if index < 0 or index >= len(sessions):
                raise ValueError(f"Invalid session index: {target}")
            path = sessions[index].path
        else:
            path_obj = Path(target).expanduser()
            if not path_obj.is_absolute():
                path_obj = self._session_manager.session_dir / target
            path = str(path_obj.resolve())
        self._session_manager.switch_session_file(path)
        self._model_controller.sync_from_session_context()
        return path

    def fork_session(self, leaf_id: str | None = None) -> str | None:
        if leaf_id is not None and leaf_id not in self._session_manager.by_id:
            return None
        source_leaf = leaf_id if leaf_id is not None else self._session_manager.leaf_id
        source_messages = self._session_manager.build_context(leaf_id=source_leaf).messages if source_leaf else []
        summary_text = generate_compaction_summary(source_messages, max_messages=8) if source_messages else None
        new_file = self._session_manager.fork_current_branch(leaf_id=leaf_id)
        if source_leaf and summary_text:
            self._session_manager.append_branch_summary(summary_text, source_leaf)
        return str(new_file) if new_file else None

    def set_session_name(self, name: str) -> None:
        self._session_manager.set_session_name(name)

    def new_session(self, parent_session: str | None = None) -> None:
        self._session_manager.new_session(parent_session=parent_session)
