from __future__ import annotations

import pytest

from gen_agent.models.content import TextContent
from gen_agent.models.messages import AssistantMessage
from gen_agent.tui.app import GenInteractiveAppV2
from gen_agent.tui.reducers import update_command_suggestions


class _DummyStatic:
    def __init__(self) -> None:
        self.value = ""

    def update(self, value: str) -> None:
        self.value = value


class _DummyRichLog:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write(self, value: str) -> None:
        self.lines.append(value)

    def clear(self) -> None:
        self.lines.clear()


class _DummyInput:
    def __init__(self) -> None:
        self.value = ""
        self.focused = False

    def focus(self) -> None:
        self.focused = True


class _DummyKey:
    def __init__(self, key: str) -> None:
        self.key = key
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


class _DummyExtRunner:
    def get_commands(self):
        return {"hello": object()}


class _DummySession:
    def __init__(self) -> None:
        self._state = {
            "provider": "openai",
            "modelId": "gpt-4o-mini",
            "thinkingLevel": "low",
            "sessionName": "demo",
            "messageCount": 3,
            "pendingMessageCount": 0,
            "steeringQueueCount": 0,
            "followUpQueueCount": 0,
        }
        self.extension_runner = _DummyExtRunner()
        self.available_tools = ["read", "bash", "edit"]
        self.session_file = "/tmp/current.jsonl"
        self.resumed_paths: list[str] = []
        self.current_leaf: str | None = None
        self.prompt_calls: list[str] = []

    def subscribe(self, _listener):
        return lambda: None

    def get_state(self):
        return dict(self._state)

    def list_sessions(self, limit: int = 20, offset: int = 0, include_current: bool = True):
        sessions = [
            {"path": "/tmp/current.jsonl", "messageCount": 3, "firstMessage": "current", "name": "current"},
            {"path": "/tmp/older.jsonl", "messageCount": 5, "firstMessage": "older", "name": "older"},
        ]
        if not include_current:
            sessions = [item for item in sessions if item["path"] != self.session_file]
        if offset:
            sessions = sessions[offset:]
        return sessions[:limit]

    def get_tree(self, limit: int | None = None, include_root: bool = False):
        entries = [
            {"id": "e1", "parentId": None, "type": "message", "timestamp": "t1"},
            {"id": "e2", "parentId": "e1", "type": "message", "timestamp": "t2"},
        ]
        if limit is not None:
            entries = entries[-max(1, limit) :]
        if include_root:
            entries = [{"id": None, "parentId": None, "type": "root", "timestamp": None}, *entries]
        return {
            "leafId": self.current_leaf,
            "entries": entries,
        }

    def resume_session(self, target: str | int) -> str:
        path = str(target)
        self.session_file = path
        self.resumed_paths.append(path)
        return path

    def switch_tree(self, leaf_id: str | None) -> bool:
        self.current_leaf = leaf_id
        return True

    def cycle_model(self, direction: str = "forward"):
        del direction
        return {"provider": "openai", "modelId": "gpt-4.1-mini"}

    def new_session(self) -> None:
        self._state["sessionName"] = "new-session"

    async def prompt(self, text: str):
        self.prompt_calls.append(text)
        return [
            AssistantMessage(
                provider="openai",
                model="gpt-4o-mini",
                content=[TextContent(text="final answer")],
                stopReason="stop",
            )
        ]


def _make_app() -> GenInteractiveAppV2:
    app = GenInteractiveAppV2(session=_DummySession())
    app.top_status_view = _DummyStatic()
    app.left_view = _DummyStatic()
    app.live_view = _DummyStatic()
    app.timeline_view = _DummyRichLog()
    app.right_view = _DummyStatic()
    app.input_view = _DummyInput()
    app._refresh_meta()
    return app


def test_refresh_meta_has_provider_and_thinking() -> None:
    app = _make_app()
    assert "provider=openai/gpt-4o-mini" in app.ui.meta_text
    assert "thinking=low" in app.ui.meta_text
    assert "session=demo" in app.ui.meta_text


def test_open_session_picker_and_confirm_selection() -> None:
    app = _make_app()
    app._open_picker("resume")
    assert app.ui.picker.mode == "resume"
    assert app.ui.picker.items

    app.ui.picker.selected_index = 1
    app._confirm_picker_selection()

    assert app.session.resumed_paths[-1] == "/tmp/older.jsonl"
    assert app.ui.picker.mode is None


def test_open_tree_picker_and_confirm_selection() -> None:
    app = _make_app()
    app._open_picker("tree")
    assert app.ui.picker.mode == "tree"
    assert app.ui.picker.items[0]["id"] is None

    app.ui.picker.selected_index = 1
    app._confirm_picker_selection()
    assert app.session.current_leaf == "e1"
    assert app.ui.picker.mode is None


@pytest.mark.asyncio
async def test_submit_adds_history_and_timeline() -> None:
    app = _make_app()
    await app._submit("hello")

    assert app.ui.input_history[-1] == "hello"
    assert any(line.startswith("You: hello") for line in app.ui.timeline_lines)
    assert any(line.startswith("Gen:") for line in app.ui.timeline_lines)


@pytest.mark.asyncio
async def test_manual_compact_routes_through_submit() -> None:
    app = _make_app()
    await app.action_manual_compact()
    assert app.session.prompt_calls[-1] == "/compact"


@pytest.mark.asyncio
async def test_focus_next_applies_selected_command_suggestion() -> None:
    app = _make_app()
    app.ui.focus = "input"
    app.input_view.value = "/re"
    update_command_suggestions(app.ui, app.input_view.value, app._command_pool())
    app.ui.selection.suggestion_index = 1

    await app.action_focus_next_pane()

    assert app.input_view.value == "/resume "
    assert app.ui.focus == "input"


@pytest.mark.asyncio
async def test_left_pane_key_navigation_and_enter_resume() -> None:
    app = _make_app()
    app.ui.focus = "left"
    app._render_all()

    down = _DummyKey("down")
    await app.on_key(down)
    assert app.ui.selection.session_index == 1
    assert down.stopped is True

    enter = _DummyKey("enter")
    await app.on_key(enter)
    assert app.session.resumed_paths[-1] == "/tmp/older.jsonl"
    assert enter.stopped is True


@pytest.mark.asyncio
async def test_left_pane_section_switch_and_quick_select_tree() -> None:
    app = _make_app()
    app.ui.focus = "left"
    app._render_all()

    right = _DummyKey("right")
    await app.on_key(right)
    assert app.ui.left_section == "tree"
    assert right.stopped is True

    quick = _DummyKey("2")
    await app.on_key(quick)
    assert app.ui.selection.tree_index == 1
    assert quick.stopped is True

    enter = _DummyKey("enter")
    await app.on_key(enter)
    assert app.session.current_leaf == "e1"
    assert enter.stopped is True


@pytest.mark.asyncio
async def test_center_pane_key_navigation_moves_timeline_selection() -> None:
    app = _make_app()
    app.ui.timeline_lines = ["a", "b", "c"]
    app.ui.focus = "center"
    app._render_all()

    down = _DummyKey("down")
    await app.on_key(down)
    assert app.ui.selection.timeline_index == 1

    pagedown = _DummyKey("pagedown")
    await app.on_key(pagedown)
    assert app.ui.selection.timeline_index == 2


@pytest.mark.asyncio
async def test_center_and_right_quick_number_selection() -> None:
    app = _make_app()
    app.ui.timeline_lines = ["a", "b", "c", "d"]
    app.ui.event_lines = ["e1", "e2", "e3"]

    app.ui.focus = "center"
    app._render_all()
    center_quick = _DummyKey("3")
    await app.on_key(center_quick)
    assert app.ui.selection.timeline_index == 2
    assert center_quick.stopped is True

    app.ui.focus = "right"
    app._render_all()
    right_quick = _DummyKey("2")
    await app.on_key(right_quick)
    assert app.ui.selection.event_index == 1
    assert right_quick.stopped is True


@pytest.mark.asyncio
async def test_right_pane_key_navigation_moves_event_selection() -> None:
    app = _make_app()
    app.ui.event_lines = ["e1", "e2", "e3"]
    app.ui.focus = "right"
    app._render_all()

    down = _DummyKey("down")
    await app.on_key(down)
    assert app.ui.selection.event_index == 1

    up = _DummyKey("up")
    await app.on_key(up)
    assert app.ui.selection.event_index == 0


@pytest.mark.asyncio
async def test_escape_clears_suggestions_then_focuses_input() -> None:
    app = _make_app()
    app.ui.focus = "left"
    app.input_view.value = "/re"
    update_command_suggestions(app.ui, app.input_view.value, app._command_pool())
    assert app.ui.command_suggestions

    await app.action_cancel_picker()
    assert app.ui.command_suggestions == []
    assert app.ui.focus == "left"

    await app.action_cancel_picker()
    assert app.ui.focus == "input"
