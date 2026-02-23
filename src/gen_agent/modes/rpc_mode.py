from __future__ import annotations

import asyncio
import contextlib
import sys
from typing import Any

import orjson
from pydantic import TypeAdapter

from gen_agent.core.agent_session import AgentSession
from gen_agent.extensions import CustomEditorComponent, NoOpExtensionUIContext
from gen_agent.models.rpc import RpcCommand, RpcResponse

_rpc_adapter = TypeAdapter(RpcCommand)


def _normalize_lines(content: Any, *, field_name: str) -> list[str] | None:
    if content is None:
        return None
    if isinstance(content, str):
        return content.splitlines() or [content]
    if isinstance(content, list):
        if not all(isinstance(line, str) for line in content):
            raise TypeError(f"{field_name} only supports str | list[str] | None")
        return content
    raise TypeError(f"{field_name} only supports str | list[str] | None")


def _normalize_widget_placement(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"beloweditor", "below_editor"}:
        return "belowEditor"
    return "aboveEditor"


def _resolve_widget_placement(value: Any) -> str:
    if isinstance(value, dict):
        return _normalize_widget_placement(str(value.get("placement", "aboveEditor")))
    if not isinstance(value, str):
        raise TypeError("widget placement must be a string or {'placement': ...}")
    return _normalize_widget_placement(str(value))


class RpcExtensionUIContext:
    def __init__(self, mode: RpcMode):
        self._mode = mode

    async def _request(
        self,
        method: str,
        payload: dict[str, Any],
        *,
        wait: bool,
        timeout: int | None,
    ) -> dict[str, Any] | None:
        request_id = self._mode._next_ui_request_id()
        self._mode._emit_ui_request(method=method, request_id=request_id, payload=payload)
        if not wait:
            return None
        return await self._mode._await_ui_response(request_id=request_id, timeout=timeout)

    async def select(self, title: str, options: list[str], timeout: int | None = None) -> str | None:
        response = await self._request(
            "select",
            {"title": title, "options": options},
            wait=True,
            timeout=timeout,
        )
        if not response or response.get("cancelled"):
            return None
        value = response.get("value")
        return value if isinstance(value, str) else None

    async def confirm(self, title: str, message: str, timeout: int | None = None) -> bool:
        response = await self._request(
            "confirm",
            {"title": title, "message": message},
            wait=True,
            timeout=timeout,
        )
        if not response or response.get("cancelled"):
            return False
        return bool(response.get("confirmed"))

    async def input(self, title: str, placeholder: str | None = None, timeout: int | None = None) -> str | None:
        response = await self._request(
            "input",
            {"title": title, "placeholder": placeholder},
            wait=True,
            timeout=timeout,
        )
        if not response or response.get("cancelled"):
            return None
        value = response.get("value")
        return value if isinstance(value, str) else None

    async def editor(self, title: str, prefill: str | None = None, timeout: int | None = None) -> str | None:
        response = await self._request(
            "editor",
            {"title": title, "prefill": prefill},
            wait=True,
            timeout=timeout,
        )
        if not response or response.get("cancelled"):
            return None
        value = response.get("value")
        return value if isinstance(value, str) else None

    def notify(self, message: str, level: str = "info") -> None:
        self._mode._emit_ui_request(
            method="notify",
            request_id=self._mode._next_ui_request_id(),
            payload={"message": message, "notifyType": level},
        )

    def set_status(self, key: str, text: str | None) -> None:
        self._mode._emit_ui_request(
            method="setStatus",
            request_id=self._mode._next_ui_request_id(),
            payload={"statusKey": key, "statusText": text},
        )

    def set_widget(self, key: str, content: Any, placement: Any = "above_editor") -> None:
        self._mode._emit_ui_request(
            method="setWidget",
            request_id=self._mode._next_ui_request_id(),
            payload={
                "widgetKey": key,
                "widgetLines": _normalize_lines(content, field_name="set_widget content"),
                "widgetPlacement": _resolve_widget_placement(placement),
            },
        )

    def set_header(self, content: Any) -> None:
        self._mode._emit_ui_request(
            method="setHeader",
            request_id=self._mode._next_ui_request_id(),
            payload={"headerLines": _normalize_lines(content, field_name="set_header content")},
        )

    def set_footer(self, content: Any) -> None:
        self._mode._emit_ui_request(
            method="setFooter",
            request_id=self._mode._next_ui_request_id(),
            payload={"footerLines": _normalize_lines(content, field_name="set_footer content")},
        )

    def set_title(self, title: str) -> None:
        self._mode._emit_ui_request(
            method="setTitle",
            request_id=self._mode._next_ui_request_id(),
            payload={"title": title},
        )

    def get_editor_text(self) -> str:
        return self._mode._rpc_editor_text

    def set_editor_text(self, text: str) -> None:
        self._mode._rpc_editor_text = text
        self._mode._emit_ui_request(
            method="setEditorText",
            request_id=self._mode._next_ui_request_id(),
            payload={"text": text},
        )

    def set_editor_component(self, component: Any) -> None:
        if component is not None and not isinstance(component, CustomEditorComponent):
            raise TypeError("set_editor_component only accepts CustomEditorComponent | None")
        payload = None
        if component is not None:
            payload = {
                "placeholder": getattr(component, "placeholder", None),
                "title": getattr(component, "title", None),
                "statusHint": getattr(component, "status_hint", None),
            }
        self._mode._emit_ui_request(
            method="setEditorComponent",
            request_id=self._mode._next_ui_request_id(),
            payload={"component": payload},
        )

    # Compatibility aliases with pi naming.
    async def selectDialog(self, title: str, options: list[str], timeout: int | None = None) -> str | None:
        return await self.select(title, options, timeout=timeout)

    async def confirmDialog(self, title: str, message: str, timeout: int | None = None) -> bool:
        return await self.confirm(title, message, timeout=timeout)

    async def inputDialog(self, title: str, placeholder: str | None = None, timeout: int | None = None) -> str | None:
        return await self.input(title, placeholder=placeholder, timeout=timeout)

    def setStatus(self, key: str, text: str | None) -> None:
        self.set_status(key, text)

    def setWidget(self, key: str, content: Any, placement: Any = "aboveEditor") -> None:
        self.set_widget(key, content, placement=placement)

    def setHeader(self, content: Any) -> None:
        self.set_header(content)

    def setFooter(self, content: Any) -> None:
        self.set_footer(content)

    def setTitle(self, title: str) -> None:
        self.set_title(title)

    def getEditorText(self) -> str:
        return self.get_editor_text()

    def setEditorText(self, text: str) -> None:
        self.set_editor_text(text)

    def setEditorComponent(self, component: Any) -> None:
        self.set_editor_component(component)


class RpcMode:
    def __init__(self, session: AgentSession):
        self.session = session
        self._active_operation_task: asyncio.Task[None] | None = None
        self._background_tasks: set[asyncio.Task[None]] = set()
        self._ui_seq = 0
        self._ui_pending: dict[str, asyncio.Future[dict[str, Any]]] = {}
        self._rpc_editor_text = ""
        if self.session.ui_extensions_enabled:
            self.session.bind_ui_context(RpcExtensionUIContext(self))
        else:
            self.session.bind_ui_context(NoOpExtensionUIContext())

    def _write(self, payload: dict) -> None:
        sys.stdout.write(orjson.dumps(payload).decode("utf-8") + "\n")
        sys.stdout.flush()

    def _response(self, command: str, success: bool, request_id: str | None = None, data=None, error: str | None = None):
        resp = RpcResponse(command=command, success=success, id=request_id, data=data, error=error)
        self._write(resp.model_dump(by_alias=True, exclude_none=True))

    def _next_ui_request_id(self) -> str:
        self._ui_seq += 1
        return f"ui_{self._ui_seq}"

    def _emit_ui_request(self, method: str, request_id: str, payload: dict[str, Any]) -> None:
        data = {
            "type": "extension_ui_request",
            "id": request_id,
            "method": method,
            **payload,
        }
        self._write(data)

    async def _await_ui_response(self, request_id: str, timeout: int | None = None) -> dict[str, Any] | None:
        loop = asyncio.get_running_loop()
        future: asyncio.Future[dict[str, Any]] = loop.create_future()
        self._ui_pending[request_id] = future
        try:
            if timeout and timeout > 0:
                return await asyncio.wait_for(future, timeout=timeout / 1000)
            return await future
        except asyncio.TimeoutError:
            return None
        finally:
            self._ui_pending.pop(request_id, None)

    def _resolve_ui_response(self, request_id: str, payload: dict[str, Any]) -> None:
        future = self._ui_pending.get(request_id)
        if future and not future.done():
            future.set_result(payload)

    async def _read_stdin_line(self) -> str:
        # Read stdin in a worker thread so long-running prompt tasks can progress.
        return await asyncio.to_thread(sys.stdin.readline)

    async def _dispatch_payload(self, payload: dict) -> None:
        try:
            await self._handle(payload)
        except asyncio.CancelledError:
            return
        except Exception as exc:
            command = payload.get("type", "unknown") if isinstance(payload, dict) else "unknown"
            request_id = payload.get("id") if isinstance(payload, dict) else None
            self._response(command, False, request_id=request_id, error=str(exc))

    def _track_background_task(self, task: asyncio.Task[None]) -> None:
        self._background_tasks.add(task)

        def _on_done(done_task: asyncio.Task[None]) -> None:
            self._background_tasks.discard(done_task)
            if self._active_operation_task is done_task:
                self._active_operation_task = None

        task.add_done_callback(_on_done)

    async def _abort_active_operation(self) -> None:
        task = self._active_operation_task
        if not task or task.done():
            return
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    async def _handle(self, raw: dict) -> None:
        cmd = _rpc_adapter.validate_python(raw)
        cid = getattr(cmd, "id", None)

        if cmd.type == "prompt":
            track_active = cmd.streaming_behavior is None
            task = asyncio.current_task() if track_active else None
            if track_active and task is not None:
                self._active_operation_task = task
            try:
                await self.session.prompt(cmd.message, images=cmd.images, streaming_behavior=cmd.streaming_behavior)
            finally:
                if track_active and self._active_operation_task is task:
                    self._active_operation_task = None
            self._response("prompt", True, cid)
            return
        if cmd.type == "steer":
            self.session.steer(cmd.message, images=cmd.images)
            self._response("steer", True, cid)
            return
        if cmd.type == "follow_up":
            self.session.follow_up(cmd.message, images=cmd.images)
            self._response("follow_up", True, cid)
            return
        if cmd.type == "abort":
            await self._abort_active_operation()
            self._response("abort", True, cid)
            return
        if cmd.type == "get_state":
            self._response("get_state", True, cid, data=self.session.get_state())
            return
        if cmd.type == "get_messages":
            messages = [m.model_dump(by_alias=True) for m in self.session.get_messages()]
            self._response("get_messages", True, cid, data={"messages": messages})
            return
        if cmd.type == "set_model":
            self.session.set_model(cmd.provider, cmd.model_id)
            self._response("set_model", True, cid, data={"provider": cmd.provider, "modelId": cmd.model_id})
            return
        if cmd.type == "new_session":
            self.session.new_session(parent_session=cmd.parent_session)
            self._response("new_session", True, cid, data={"cancelled": False})
            return
        if cmd.type == "continue":
            task = asyncio.current_task()
            if task is not None:
                self._active_operation_task = task
            try:
                await self.session.continue_run()
            finally:
                if self._active_operation_task is task:
                    self._active_operation_task = None
            self._response("continue", True, cid)
            return
        if cmd.type == "cycle_model":
            data = self.session.cycle_model()
            self._response("cycle_model", True, cid, data=data)
            return
        if cmd.type == "set_thinking_level":
            self.session.set_thinking_level(cmd.level)
            self._response("set_thinking_level", True, cid)
            return
        if cmd.type == "set_steering_mode":
            self.session.set_steering_mode(cmd.mode)
            self._response("set_steering_mode", True, cid)
            return
        if cmd.type == "set_follow_up_mode":
            self.session.set_follow_up_mode(cmd.mode)
            self._response("set_follow_up_mode", True, cid)
            return
        if cmd.type == "set_session_name":
            self.session.set_session_name(cmd.name)
            self._response("set_session_name", True, cid)
            return
        if cmd.type == "get_tree":
            self._response("get_tree", True, cid, data=self.session.get_tree())
            return
        if cmd.type == "switch_tree":
            leaf_id = cmd.leaf_id
            if leaf_id in {"root", "none", ""}:
                leaf_id = None
            ok = self.session.switch_tree(leaf_id)
            if not ok:
                self._response("switch_tree", False, cid, error=f"Unknown tree leaf: {cmd.leaf_id}")
                return
            self._response("switch_tree", True, cid, data={"leafId": self.session.session_manager.leaf_id})
            return
        if cmd.type == "list_sessions":
            sessions = self.session.list_sessions(limit=cmd.limit)
            self._response("list_sessions", True, cid, data={"sessions": sessions})
            return
        if cmd.type == "resume_session":
            target = cmd.index if cmd.index is not None else cmd.path
            if target is None:
                self._response("resume_session", False, cid, error="resume_session requires index or path")
                return
            path = self.session.resume_session(target)
            self._response("resume_session", True, cid, data={"sessionFile": path})
            return
        if cmd.type == "fork_session":
            new_file = self.session.fork_session(leaf_id=cmd.leaf_id)
            if cmd.leaf_id is not None and new_file is None:
                self._response("fork_session", False, cid, error=f"Unknown tree leaf: {cmd.leaf_id}")
                return
            self._response("fork_session", True, cid, data={"sessionFile": new_file})
            return
        if cmd.type == "compact":
            result = self.session.compact_now()
            self._response("compact", True, cid, data={"message": result})
            return
        if cmd.type == "reload":
            diagnostics = self.session.reload_resources()
            self._response("reload", True, cid, data={"diagnostics": diagnostics})
            return
        if cmd.type == "extension_ui_response":
            payload: dict[str, Any] = {}
            if cmd.value is not None:
                payload["value"] = cmd.value
            if cmd.confirmed is not None:
                payload["confirmed"] = cmd.confirmed
            if cmd.cancelled is not None:
                payload["cancelled"] = cmd.cancelled
            self._resolve_ui_response(cmd.id, payload)
            return

        self._response(cmd.type, False, cid, error="Unsupported command")

    async def run(self) -> int:
        def on_event(event):
            self._write(event.model_dump(by_alias=True))

        unsub = self.session.subscribe(on_event)
        try:
            while True:
                line = await self._read_stdin_line()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = orjson.loads(line)
                except Exception as exc:
                    self._response("unknown", False, error=f"Invalid JSON: {exc}")
                    continue

                command_type = payload.get("type") if isinstance(payload, dict) else None
                if command_type in {"prompt", "continue"}:
                    active_task = self._active_operation_task
                    if active_task and not active_task.done():
                        request_id = payload.get("id") if isinstance(payload, dict) else None
                        if command_type == "prompt" and payload.get("streamingBehavior") in {"steer", "followUp"}:
                            await self._dispatch_payload(payload)
                        else:
                            self._response(
                                command_type,
                                False,
                                request_id=request_id,
                                error="Agent is already running. Use prompt with streamingBehavior=steer|followUp or abort.",
                            )
                        continue

                    task = asyncio.create_task(self._dispatch_payload(payload))
                    self._active_operation_task = task
                    self._track_background_task(task)
                    continue

                await self._dispatch_payload(payload)
        finally:
            for task in list(self._background_tasks):
                task.cancel()
            if self._background_tasks:
                await asyncio.gather(*self._background_tasks, return_exceptions=True)
            for request_id, future in list(self._ui_pending.items()):
                if not future.done():
                    future.set_result({"cancelled": True})
                self._ui_pending.pop(request_id, None)
            unsub()
            self.session.bind_ui_context(NoOpExtensionUIContext())

        return 0


async def run_rpc_mode(session: AgentSession) -> int:
    return await RpcMode(session).run()
