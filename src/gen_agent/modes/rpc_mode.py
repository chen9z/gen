from __future__ import annotations

import asyncio
import contextlib
import sys

import orjson
from pydantic import TypeAdapter

from gen_agent.core.agent_session import AgentSession
from gen_agent.models.rpc import RpcCommand, RpcResponse

_rpc_adapter = TypeAdapter(RpcCommand)


class RpcMode:
    def __init__(self, session: AgentSession):
        self.session = session
        self._active_operation_task: asyncio.Task[None] | None = None
        self._background_tasks: set[asyncio.Task[None]] = set()

    def _write(self, payload: dict) -> None:
        sys.stdout.write(orjson.dumps(payload).decode("utf-8") + "\n")
        sys.stdout.flush()

    def _response(self, command: str, success: bool, request_id: str | None = None, data=None, error: str | None = None):
        resp = RpcResponse(command=command, success=success, id=request_id, data=data, error=error)
        self._write(resp.model_dump(by_alias=True, exclude_none=True))

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
            unsub()

        return 0


async def run_rpc_mode(session: AgentSession) -> int:
    return await RpcMode(session).run()
