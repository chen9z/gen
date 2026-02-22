from __future__ import annotations

from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.widgets import Footer, Header, Input, RichLog, Static

from gen_agent.core.agent_session import AgentSession

from .reducers import (
    apply_selected_suggestion,
    apply_input_history,
    close_picker,
    focus_next,
    focus_prev,
    history_next,
    history_prev,
    move_picker_selection,
    move_suggestion_selection,
    open_picker,
    page_picker_selection,
    reduce_session_event,
    select_picker_by_number,
    selected_suggestion,
    update_command_suggestions,
)
from .state import PaneFocus, UIState
from .widgets import render_inspector, render_left_panel, render_live_panel

_LEFT_SECTIONS = ["sessions", "tree", "tools"]
_LEFT_SESSIONS_MAX = 9
_LEFT_TREE_MAX = 8
_LEFT_TOOLS_MAX = 10


class GenInteractiveAppV2(App):
    CSS = """
    #layout {
        layout: vertical;
    }
    #top_status {
        height: 2;
    }
    #body {
        layout: horizontal;
        height: 1fr;
    }
    #left_pane {
        width: 34;
        border: round $primary;
        padding: 0 1;
    }
    #center_pane {
        width: 1fr;
        border: round $accent;
        padding: 0 1;
    }
    #right_pane {
        width: 44;
        border: round $secondary;
        padding: 0 1;
    }
    #live {
        height: 12;
        border: round $surface;
        padding: 0 1;
    }
    #timeline {
        height: 1fr;
        border: round $surface;
    }
    #input {
        height: 3;
    }
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "cycle_model", "Cycle model"),
        ("ctrl+p", "cycle_model", "Cycle model"),
        ("ctrl+shift+p", "cycle_model_backward", "Cycle model back"),
        ("ctrl+n", "new_session", "New session"),
        ("ctrl+r", "open_session_picker", "Sessions"),
        ("ctrl+t", "open_tree_picker", "Tree"),
        ("ctrl+k", "manual_compact", "Compact"),
        ("tab", "focus_next_pane", "Next pane"),
        ("shift+tab", "focus_prev_pane", "Prev pane"),
        ("escape", "cancel_picker", "Cancel"),
        ("ctrl+u", "clear_input", "Clear input"),
    ]

    def __init__(self, session: AgentSession, initial_prompt: str | None = None):
        super().__init__()
        self.session = session
        self.initial_prompt = initial_prompt
        self.ui = UIState()
        self._unsubscribe = None

        self.top_status_view: Static
        self.left_view: Static
        self.live_view: Static
        self.timeline_view: RichLog
        self.right_view: Static
        self.input_view: Input

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Container(id="layout"):
            yield Static("status", id="top_status")
            with Container(id="body"):
                yield Static("", id="left_pane")
                with Container(id="center_pane"):
                    yield Static("", id="live")
                    yield RichLog(id="timeline", wrap=True, auto_scroll=True)
                yield Static("", id="right_pane")
            yield Input(placeholder="Type message or /command", id="input")
        yield Footer()

    async def on_mount(self) -> None:
        self.top_status_view = self.query_one("#top_status", Static)
        self.left_view = self.query_one("#left_pane", Static)
        self.live_view = self.query_one("#live", Static)
        self.timeline_view = self.query_one("#timeline", RichLog)
        self.right_view = self.query_one("#right_pane", Static)
        self.input_view = self.query_one("#input", Input)

        self._unsubscribe = self.session.subscribe(self._on_session_event)
        self._refresh_meta()
        self._render_all()
        self.input_view.focus()

        self.timeline_view.write(
            "[dim]Shortcuts: Ctrl+L/Ctrl+P model, Ctrl+Shift+P back, Ctrl+N new, Ctrl+R sessions, Ctrl+T tree, Ctrl+K compact, "
            "Tab panes, Left/Right section, 1-9 quick select, Esc cancel[/dim]"
        )

        if self.initial_prompt:
            await self._submit(self.initial_prompt)

    async def on_unmount(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    def _refresh_meta(self) -> None:
        state = self.session.get_state()
        session_name = state.get("sessionName") or "-"
        self.ui.meta_text = (
            f"provider={state['provider']}/{state['modelId']} | thinking={state['thinkingLevel']} "
            f"| session={session_name} | messages={state['messageCount']} "
            f"| pending={state['pendingMessageCount']} (steer={state['steeringQueueCount']}, follow={state['followUpQueueCount']})"
        )
        self.ui.status_text = "Ready"

    def _get_session_list(self) -> list[dict[str, Any]]:
        return self.session.list_sessions(limit=20, offset=0, include_current=True)

    def _get_tree_entries(self) -> list[dict[str, Any]]:
        tree = self.session.get_tree(limit=50, include_root=True)
        return tree.get("entries") or []

    def _get_tools(self) -> list[str]:
        return self.session.available_tools

    def _get_left_panel_data(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
        sessions = self._get_session_list()[:_LEFT_SESSIONS_MAX]
        trees = self._get_tree_entries()
        if len(trees) > _LEFT_TREE_MAX:
            trees = trees[-_LEFT_TREE_MAX:]
        tools = self._get_tools()[:_LEFT_TOOLS_MAX]
        return sessions, trees, tools

    def _render_timeline(self) -> None:
        self.timeline_view.clear()
        for line in self.ui.timeline_lines[-400:]:
            self.timeline_view.write(line)

    def _render_all(self) -> None:
        current_file = getattr(self.session, "session_file", None)
        sessions, trees, tools = self._get_left_panel_data()
        self._clamp_selection(sessions, trees, tools)
        self.top_status_view.update(f"{self.ui.meta_text}\nstatus={self.ui.status_text}")
        self.left_view.update(render_left_panel(self.ui, sessions, trees, tools))
        self.live_view.update(render_live_panel(self.ui))
        self.right_view.update(render_inspector(self.ui, current_file, sessions, trees, tools))
        self._render_timeline()

    def _clamp_selection(self, sessions: list[dict[str, Any]], trees: list[dict[str, Any]], tools: list[str]) -> None:
        if sessions:
            self.ui.selection.session_index = min(max(0, self.ui.selection.session_index), len(sessions) - 1)
        else:
            self.ui.selection.session_index = 0
        if trees:
            self.ui.selection.tree_index = min(max(0, self.ui.selection.tree_index), len(trees) - 1)
        else:
            self.ui.selection.tree_index = 0
        if tools:
            self.ui.selection.tool_index = min(max(0, self.ui.selection.tool_index), len(tools) - 1)
        else:
            self.ui.selection.tool_index = 0
        if self.ui.timeline_lines:
            self.ui.selection.timeline_index = min(max(0, self.ui.selection.timeline_index), len(self.ui.timeline_lines) - 1)
        else:
            self.ui.selection.timeline_index = 0
        if self.ui.event_lines:
            self.ui.selection.event_index = min(max(0, self.ui.selection.event_index), len(self.ui.event_lines) - 1)
        else:
            self.ui.selection.event_index = 0

    def _move_left_section(self, delta: int) -> None:
        idx = _LEFT_SECTIONS.index(self.ui.left_section)
        self.ui.left_section = _LEFT_SECTIONS[(idx + delta) % len(_LEFT_SECTIONS)]  # type: ignore[assignment]

    def _move_left_selection(self, delta: int, sessions: list[dict[str, Any]], trees: list[dict[str, Any]], tools: list[str]) -> None:
        if self.ui.left_section == "sessions" and sessions:
            self.ui.selection.session_index = (self.ui.selection.session_index + delta) % len(sessions)
            return
        if self.ui.left_section == "tree" and trees:
            self.ui.selection.tree_index = (self.ui.selection.tree_index + delta) % len(trees)
            return
        if self.ui.left_section == "tools" and tools:
            self.ui.selection.tool_index = (self.ui.selection.tool_index + delta) % len(tools)

    def _page_left_selection(
        self,
        delta_pages: int,
        sessions: list[dict[str, Any]],
        trees: list[dict[str, Any]],
        tools: list[str],
        page_size: int = 5,
    ) -> None:
        delta = delta_pages * page_size
        if self.ui.left_section == "sessions" and sessions:
            self.ui.selection.session_index = min(max(0, self.ui.selection.session_index + delta), len(sessions) - 1)
            return
        if self.ui.left_section == "tree" and trees:
            self.ui.selection.tree_index = min(max(0, self.ui.selection.tree_index + delta), len(trees) - 1)
            return
        if self.ui.left_section == "tools" and tools:
            self.ui.selection.tool_index = min(max(0, self.ui.selection.tool_index + delta), len(tools) - 1)

    def _apply_quick_select_left(
        self,
        number: int,
        sessions: list[dict[str, Any]],
        trees: list[dict[str, Any]],
        tools: list[str],
    ) -> bool:
        index = number - 1
        if self.ui.left_section == "sessions" and 0 <= index < len(sessions):
            self.ui.selection.session_index = index
            return True
        if self.ui.left_section == "tree" and 0 <= index < len(trees):
            self.ui.selection.tree_index = index
            return True
        if self.ui.left_section == "tools" and 0 <= index < len(tools):
            self.ui.selection.tool_index = index
            return True
        return False

    def _confirm_left_selection(self, sessions: list[dict[str, Any]], trees: list[dict[str, Any]], tools: list[str]) -> None:
        if self.ui.left_section == "sessions":
            if not sessions:
                self.ui.event_lines.append("No sessions to select.")
                return
            target = sessions[self.ui.selection.session_index]["path"]
            resumed = self.session.resume_session(target)
            self.ui.event_lines.append(f"Resumed: {resumed}")
            self._refresh_meta()
            return
        if self.ui.left_section == "tree":
            if not trees:
                self.ui.event_lines.append("No tree entries to select.")
                return
            leaf_id = trees[self.ui.selection.tree_index].get("id")
            if self.session.switch_tree(leaf_id):
                token = "root" if leaf_id is None else str(leaf_id)
                self.ui.event_lines.append(f"Tree leaf: {token}")
            else:
                self.ui.event_lines.append(f"Unknown tree leaf: {leaf_id}")
            return
        if self.ui.left_section == "tools":
            if not tools:
                self.ui.event_lines.append("No tools to select.")
                return
            tool = tools[self.ui.selection.tool_index]
            self.ui.event_lines.append(f"Tool selected: {tool}")

    def _set_focus(self, focus: PaneFocus) -> None:
        self.ui.focus = focus
        if focus == "input":
            self.input_view.focus()
        self._render_all()

    def _open_picker(self, mode: str) -> None:
        if mode == "resume":
            items = self._get_session_list()
            if not items:
                self.ui.event_lines.append("No previous sessions found.")
                self._render_all()
                return
            open_picker(self.ui, "resume", items)
        else:
            open_picker(self.ui, "tree", self._get_tree_entries())
        self._render_all()

    def _apply_suggestion_to_input(self) -> bool:
        suggestion = selected_suggestion(self.ui)
        if suggestion is None:
            return False
        self.input_view.value = apply_selected_suggestion(self.ui, self.input_view.value)
        update_command_suggestions(self.ui, self.input_view.value, self._command_pool())
        self._render_all()
        return True

    def _confirm_picker_selection(self) -> None:
        if not self.ui.picker.is_open or not self.ui.picker.items:
            return
        index = self.ui.picker.selected_index
        if index < 0 or index >= len(self.ui.picker.items):
            return
        item = self.ui.picker.items[index]
        try:
            if self.ui.picker.mode == "resume":
                path = str(item.get("path") or "")
                if not path:
                    self.ui.event_lines.append("Invalid session item.")
                else:
                    resumed = self.session.resume_session(path)
                    self.ui.event_lines.append(f"Resumed: {resumed}")
            elif self.ui.picker.mode == "tree":
                leaf_id = item.get("id")
                if self.session.switch_tree(leaf_id):
                    token = "root" if leaf_id is None else str(leaf_id)
                    self.ui.event_lines.append(f"Tree leaf: {token}")
                else:
                    self.ui.event_lines.append(f"Unknown tree leaf: {leaf_id}")
        except Exception as exc:
            self.ui.event_lines.append(f"Picker error: {exc}")
        close_picker(self.ui)
        self._refresh_meta()
        self._render_all()

    def _handle_picker_text(self, text: str) -> bool:
        if not self.ui.picker.is_open:
            return False
        value = text.strip().lower()
        if value in {"q", "quit", "cancel"}:
            self.ui.event_lines.append("Picker cancelled")
            close_picker(self.ui)
            self._render_all()
            return True
        if value.isdigit():
            number = int(value)
            if not select_picker_by_number(self.ui, number):
                self.ui.event_lines.append("Index out of range")
                self._render_all()
                return True
            self._confirm_picker_selection()
            return True
        self.ui.event_lines.append("Please enter an index number, or Esc/cancel.")
        self._render_all()
        return True

    def _command_pool(self) -> list[str]:
        builtins = [
            "settings",
            "model",
            "scoped-models",
            "name",
            "session",
            "fork",
            "tree",
            "new",
            "resume",
            "compact",
            "reload",
            "quit",
        ]
        ext = sorted(self.session.extension_runner.get_commands().keys())
        return sorted(dict.fromkeys([*builtins, *ext]))

    def _on_session_event(self, event) -> None:
        reduce_session_event(self.ui, event)
        if event.type == "agent_end":
            self._refresh_meta()
        self._render_all()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        event.input.value = ""
        update_command_suggestions(self.ui, "", self._command_pool())
        if not text:
            return
        if self._handle_picker_text(text):
            return
        await self._submit(text)

    async def on_input_changed(self, event: Input.Changed) -> None:
        update_command_suggestions(self.ui, event.value, self._command_pool())
        self._render_all()

    async def on_key(self, event: Key) -> None:
        if self.ui.picker.is_open:
            if event.key == "up":
                move_picker_selection(self.ui, -1)
                self._render_all()
                event.stop()
                return
            if event.key == "down":
                move_picker_selection(self.ui, 1)
                self._render_all()
                event.stop()
                return
            if event.key == "pageup":
                page_picker_selection(self.ui, -1)
                self._render_all()
                event.stop()
                return
            if event.key == "pagedown":
                page_picker_selection(self.ui, 1)
                self._render_all()
                event.stop()
                return
            if event.key == "enter":
                self._confirm_picker_selection()
                event.stop()
                return
            if event.key.isdigit() and "1" <= event.key <= "9":
                select_picker_by_number(self.ui, int(event.key))
                self._confirm_picker_selection()
                event.stop()
                return

        if not self.ui.picker.is_open and self.ui.focus == "left":
            sessions, trees, tools = self._get_left_panel_data()
            self._clamp_selection(sessions, trees, tools)

            if event.key == "left":
                self._move_left_section(-1)
                self._render_all()
                event.stop()
                return
            if event.key == "right":
                self._move_left_section(1)
                self._render_all()
                event.stop()
                return
            if event.key == "up":
                self._move_left_selection(-1, sessions, trees, tools)
                self._render_all()
                event.stop()
                return
            if event.key == "down":
                self._move_left_selection(1, sessions, trees, tools)
                self._render_all()
                event.stop()
                return
            if event.key == "pageup":
                self._page_left_selection(-1, sessions, trees, tools)
                self._render_all()
                event.stop()
                return
            if event.key == "pagedown":
                self._page_left_selection(1, sessions, trees, tools)
                self._render_all()
                event.stop()
                return
            if event.key == "enter":
                self._confirm_left_selection(sessions, trees, tools)
                self._render_all()
                event.stop()
                return
            if event.key.isdigit() and "1" <= event.key <= "9":
                if self._apply_quick_select_left(int(event.key), sessions, trees, tools):
                    self._render_all()
                else:
                    self.ui.event_lines.append(f"Index {event.key} out of range for {self.ui.left_section}.")
                    self._render_all()
                event.stop()
                return

        if not self.ui.picker.is_open and self.ui.focus == "center":
            if event.key == "up":
                if self.ui.timeline_lines:
                    self.ui.selection.timeline_index = max(0, self.ui.selection.timeline_index - 1)
                self._render_all()
                event.stop()
                return
            if event.key == "down":
                if self.ui.timeline_lines:
                    self.ui.selection.timeline_index = min(len(self.ui.timeline_lines) - 1, self.ui.selection.timeline_index + 1)
                self._render_all()
                event.stop()
                return
            if event.key == "pageup":
                if self.ui.timeline_lines:
                    self.ui.selection.timeline_index = max(0, self.ui.selection.timeline_index - 10)
                self._render_all()
                event.stop()
                return
            if event.key == "pagedown":
                if self.ui.timeline_lines:
                    self.ui.selection.timeline_index = min(len(self.ui.timeline_lines) - 1, self.ui.selection.timeline_index + 10)
                self._render_all()
                event.stop()
                return
            if event.key.isdigit() and "1" <= event.key <= "9":
                index = int(event.key) - 1
                if index < len(self.ui.timeline_lines):
                    self.ui.selection.timeline_index = index
                else:
                    self.ui.event_lines.append(f"Timeline index {event.key} out of range.")
                self._render_all()
                event.stop()
                return

        if not self.ui.picker.is_open and self.ui.focus == "right":
            if event.key == "up":
                if self.ui.event_lines:
                    self.ui.selection.event_index = max(0, self.ui.selection.event_index - 1)
                self._render_all()
                event.stop()
                return
            if event.key == "down":
                if self.ui.event_lines:
                    self.ui.selection.event_index = min(len(self.ui.event_lines) - 1, self.ui.selection.event_index + 1)
                self._render_all()
                event.stop()
                return
            if event.key == "pageup":
                if self.ui.event_lines:
                    self.ui.selection.event_index = max(0, self.ui.selection.event_index - 10)
                self._render_all()
                event.stop()
                return
            if event.key == "pagedown":
                if self.ui.event_lines:
                    self.ui.selection.event_index = min(len(self.ui.event_lines) - 1, self.ui.selection.event_index + 10)
                self._render_all()
                event.stop()
                return
            if event.key.isdigit() and "1" <= event.key <= "9":
                index = int(event.key) - 1
                if index < len(self.ui.event_lines):
                    self.ui.selection.event_index = index
                else:
                    self.ui.event_lines.append(f"Event index {event.key} out of range.")
                self._render_all()
                event.stop()
                return

        if self.ui.focus == "input" and not self.ui.picker.is_open:
            if self.ui.command_suggestions:
                if event.key == "up":
                    move_suggestion_selection(self.ui, -1)
                    self._render_all()
                    event.stop()
                    return
                if event.key == "down":
                    move_suggestion_selection(self.ui, 1)
                    self._render_all()
                    event.stop()
                    return
                if event.key == "enter":
                    if self._apply_suggestion_to_input():
                        event.stop()
                        return
            if event.key == "up":
                self.input_view.value = history_prev(self.ui, self.input_view.value)
                event.stop()
                return
            if event.key == "down":
                self.input_view.value = history_next(self.ui)
                event.stop()
                return

    async def _submit(self, text: str) -> None:
        self.ui.timeline_lines.append(f"You: {text}")
        apply_input_history(self.ui, text)
        self.ui.status_text = "Working..."
        self._render_all()
        try:
            new_messages = await self.session.prompt(text)
            for msg in new_messages:
                role = getattr(msg, "role", "")
                if role == "assistant":
                    content = getattr(msg, "content", [])
                    parts = [block.text for block in content if getattr(block, "type", "") == "text"]
                    if parts:
                        joined = "\n".join(parts)
                        self.ui.timeline_lines.append(f"Gen: {joined}")
                elif role == "toolResult":
                    content = getattr(msg, "content", [])
                    parts = [block.text for block in content if getattr(block, "type", "") == "text"]
                    if parts:
                        joined = "\n".join(parts)
                        self.ui.timeline_lines.append(f"Tool result: {joined}")
        except SystemExit:
            self.exit()
            return
        except Exception as exc:
            self.ui.timeline_lines.append(f"Error: {exc}")
        finally:
            self.ui.status_text = "Ready"
            self._refresh_meta()
            self._render_all()

    async def action_focus_next_pane(self) -> None:
        if self.ui.focus == "input" and self.ui.command_suggestions:
            if self._apply_suggestion_to_input():
                return
        focus_next(self.ui)
        self._set_focus(self.ui.focus)

    async def action_focus_prev_pane(self) -> None:
        focus_prev(self.ui)
        self._set_focus(self.ui.focus)

    async def action_cycle_model(self) -> None:
        result = self.session.cycle_model()
        self.ui.event_lines.append(f"Model: {result['provider']}/{result['modelId']}")
        self._refresh_meta()
        self._render_all()

    async def action_cycle_model_backward(self) -> None:
        result = self.session.cycle_model(direction="backward")
        self.ui.event_lines.append(f"Model: {result['provider']}/{result['modelId']}")
        self._refresh_meta()
        self._render_all()

    async def action_new_session(self) -> None:
        self.session.new_session()
        self.ui.event_lines.append("Session: started new session")
        self._refresh_meta()
        self._render_all()

    async def action_open_session_picker(self) -> None:
        self._open_picker("resume")

    async def action_open_tree_picker(self) -> None:
        self._open_picker("tree")

    async def action_manual_compact(self) -> None:
        await self._submit("/compact")

    async def action_cancel_picker(self) -> None:
        if self.ui.picker.is_open:
            self.ui.event_lines.append("Picker cancelled")
            close_picker(self.ui)
            self._render_all()
            return
        if self.ui.command_suggestions:
            update_command_suggestions(self.ui, "", self._command_pool())
            self._render_all()
            return
        if self.ui.focus != "input":
            self._set_focus("input")

    async def action_clear_input(self) -> None:
        self.input_view.value = ""
        update_command_suggestions(self.ui, "", self._command_pool())
        self._render_all()


async def run_interactive_mode(session: AgentSession, initial_message: str | None = None) -> int:
    app = GenInteractiveAppV2(session=session, initial_prompt=initial_message)
    await app.run_async()
    return 0
