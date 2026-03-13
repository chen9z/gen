# Interactive UI Simplification Design

**Date:** 2026-03-13
**Status:** Draft
**Reference:** `/Users/looper/workspace/bub` (Bub project)

## Problem

The current interactive UI in `src/gen_agent/interactive/` consists of 22 files and 3,394 lines of code. It includes adaptive refresh rates, 3-layer state management, extension UI bridges, picker dialogs, streaming syntax highlighting, diff renderers, and 8 keyboard shortcuts. This complexity is disproportionate to the user-facing value it delivers.

The reference project Bub achieves a fully functional interactive CLI with 4 files and 428 lines, using the same technology stack (prompt_toolkit + Rich).

## Goal

Rewrite the interactive UI following Bub's minimal architecture pattern. Target: **3 files, ~400 lines**. Retain streaming output and tool call display. Remove everything else.

## Design

### New File Structure

```
src/gen_agent/interactive/
├── app.py          (~200 lines)  — REPL loop + command dispatch + prompt input
├── stream_view.py  (~150 lines)  — Rich.Live streaming + event processing + tool display
└── __init__.py     (~50 lines)   — Public API + run_interactive_mode entry point
```

All other files in `interactive/` are deleted (19 files removed).

### app.py — InteractiveApp (~200 lines)

Merges: `ptk_app.py`, `prompt_session.py`, `keymap.py`, `completers.py`, `history.py`, `pickers.py`, `shortcuts_dialog.py`.

```python
class InteractiveApp:
    """Minimal interactive REPL for gen-agent."""

    def __init__(self, session: AgentSession, console: Console):
        self._session = session
        self._console = console
        self._prompt = self._build_prompt()

    async def run(self) -> int:
        """Main REPL loop."""
        self._print_welcome()
        while True:
            try:
                text = await self._prompt.prompt_async()
            except (EOFError, KeyboardInterrupt):
                break
            text = text.strip()
            if not text:
                continue
            if text.startswith("/"):
                if await self._handle_command(text):
                    break  # /quit
            else:
                await self._run_agent(text)
        return 0

    async def _run_agent(self, prompt: str):
        """Run agent with streaming display."""
        view = StreamView(self._console)
        view.start()
        # Forward session events to stream_view
        # ... session.run(prompt) with event callback view.on_event
        view.stop()
        # Print final output to scrollback
        view.print_final(self._console)

    async def _handle_command(self, text: str) -> bool:
        """Dispatch /commands. Returns True for /quit."""
        cmd, _, arg = text.partition(" ")
        match cmd:
            case "/quit":
                return True
            case "/model":
                self._handle_model(arg.strip())
            case "/resume":
                await self._handle_resume(arg.strip())
            case "/compact":
                await self._handle_compact()
            case "/help":
                self._print_help()
            case _:
                self._console.print(f"[red]Unknown command: {cmd}[/red]")
        return False

    def _build_prompt(self) -> PromptSession:
        """Create prompt_toolkit session with minimal config."""
        commands = ["/quit", "/model", "/resume", "/help", "/compact"]
        return PromptSession(
            message="> ",
            completer=WordCompleter(commands, sentence=True),
            history=FileHistory(self._history_path()),
        )
```

**Key decisions:**
- `PromptSession` with `WordCompleter` — no fuzzy matching, no @ path completion.
- `FileHistory` — reuse prompt_toolkit's built-in, no custom `HistoryStore`.
- No keyboard shortcuts beyond Ctrl+C (handled by `KeyboardInterrupt`).
- Commands use `match/case` dispatch — no command pool or extension commands.
- `/resume [id]` lists sessions to console when no arg, resumes when given ID.
- `/model [name]` lists available models when no arg, switches when given name.

### stream_view.py — StreamView (~150 lines)

Merges: `live_view.py`, `event_processor.py`, `state_manager.py`, `render_engine.py`, `commit_manager.py`, `blocks.py`, `renderers.py`, `syntax_highlighter.py`, `diff_renderer.py`, `theme.py`, `data_models.py`, `tool_key_args.py`, `layout.py`, `render.py`.

```python
@dataclass
class ToolStatus:
    """Minimal tool call tracking."""
    name: str
    args_summary: str = ""
    status: Literal["running", "done", "error"] = "running"
    duration: float = 0.0
    is_error: bool = False

class StreamView:
    """Streams agent output via Rich.Live."""

    def __init__(self, console: Console):
        self._console = console
        self._live = Live(console=console, refresh_per_second=10)
        self._text_parts: list[str] = []
        self._tools: dict[str, ToolStatus] = {}
        self._working = False
        self._error: str | None = None

    def start(self):
        self._live.start()

    def stop(self):
        self._live.stop()

    def on_event(self, event: AgentSessionEvent):
        """Dispatch event to update state, then refresh."""
        match event.type:
            case "agent_start":
                self._working = True
                self._text_parts.clear()
                self._tools.clear()
            case "message_update":
                self._on_message_update(event)
            case "tool_execution_start":
                tool = event.tool_execution
                self._tools[tool.call_id] = ToolStatus(
                    name=tool.name,
                    args_summary=_summarize_args(tool.args),
                )
            case "tool_execution_end":
                tool = event.tool_execution
                ts = self._tools.get(tool.call_id)
                if ts:
                    ts.status = "error" if tool.is_error else "done"
                    ts.duration = tool.duration
                    ts.is_error = tool.is_error
            case "agent_end":
                self._working = False
        self._refresh()

    def _on_message_update(self, event):
        """Handle streaming text deltas."""
        msg = event.assistant_message_event
        match msg.type:
            case "text_delta":
                self._text_parts.append(msg.delta)
            case "error":
                self._error = msg.error

    def _refresh(self):
        """Build renderable group and update Live."""
        parts = []
        text = "".join(self._text_parts)
        if text:
            parts.append(Markdown(text))
        for ts in self._tools.values():
            parts.append(self._render_tool(ts))
        if self._working:
            parts.append(Spinner("dots", style="cyan"))
        self._live.update(Group(*parts) if parts else Text(""))

    def _render_tool(self, ts: ToolStatus) -> Text:
        """Render a single tool call status line."""
        if ts.status == "running":
            return Text(f"  ⠋ {ts.name} {ts.args_summary} ...", style="yellow")
        icon = "✓" if not ts.is_error else "✗"
        color = "green" if not ts.is_error else "red"
        return Text(f"  {icon} {ts.name} {ts.args_summary} ({ts.duration:.1f}s)", style=color)

    def print_final(self, console: Console):
        """Print completed output to scrollback."""
        text = "".join(self._text_parts)
        if text:
            console.print(Markdown(text))
        for ts in self._tools.values():
            console.print(self._render_tool(ts))
```

**Key decisions:**
- State is 3 instance variables: `_text_parts`, `_tools`, `_working`. No separate StateManager.
- No adaptive refresh — `Rich.Live(refresh_per_second=10)` handles rate limiting.
- No streaming syntax highlighter — `Rich.Markdown` uses Pygments internally.
- No commit manager — `print_final()` outputs completed content to scrollback after `stop()`.
- No diff renderer — tool results shown as status lines, no expandable details.
- No theme system — use Rich's default styles directly.
- `_text_parts` uses list accumulation (`"".join()`) for O(n) text building.

### __init__.py — Public API (~50 lines)

```python
from .app import InteractiveApp
from .stream_view import StreamView

async def run_interactive_mode(session, initial_message=None, console=None):
    """Entry point for interactive mode."""
    console = console or Console()
    app = InteractiveApp(session, console)
    if initial_message:
        await app._run_agent(initial_message)
    return await app.run()

__all__ = ["InteractiveApp", "StreamView", "run_interactive_mode"]
```

### Extension UI Impact

`extensions/ui.py` defines `ExtensionUIContext` protocol and `NoOpExtensionUIContext`. These stay **unchanged**. The current interactive mode's `PtkExtensionUIContext` implementation is deleted — extensions will use the no-op fallback. No adapter code needed.

### External References to Update

| File | Current Import | Change |
|------|---------------|--------|
| `modes/interactive_mode.py` | `from gen_agent.interactive.ptk_app import GenInteractiveApp, run_interactive_mode` | Update to `from gen_agent.interactive import InteractiveApp, run_interactive_mode` |
| `modes/interactive_mode.py` | `from gen_agent.interactive.blocks import LIVE_CHAR_LIMIT` | Remove (no longer needed) |

### Tests to Rewrite

| Current Test | Action |
|-------------|--------|
| `tests/unit/test_interactive_live_view.py` | Rewrite for `StreamView` |
| `tests/unit/test_interactive_mode.py` | Rewrite for `InteractiveApp` |
| `tests/unit/test_interactive_history.py` | Delete (using built-in `FileHistory`) |
| `tests/unit/test_interactive_prompt_session.py` | Delete (no custom prompt session) |
| `tests/unit/test_interactive_completers.py` | Delete (using `WordCompleter`) |
| `tests/unit/test_interactive_reducers.py` | Delete (no reducers) |
| `tests/integration/test_interactive_flow.py` | Rewrite for new API |

## What Gets Deleted

### Files Deleted (19 of 22)

- `ptk_app.py` (412L) — replaced by `app.py`
- `live_view.py` (532L) — replaced by `stream_view.py`
- `event_processor.py` (396L) — inlined into `stream_view.py`
- `state_manager.py` (187L) — state is instance vars on `StreamView`
- `render_engine.py` (184L) — `Rich.Live` handles refresh
- `blocks.py` (279L) — replaced by `ToolStatus` dataclass
- `renderers.py` (129L) — inlined into `stream_view.py`
- `prompt_session.py` (117L) — inlined into `app.py`
- `completers.py` (167L) — replaced by `WordCompleter`
- `diff_renderer.py` (151L) — removed entirely
- `syntax_highlighter.py` (144L) — `Rich.Markdown` handles this
- `theme.py` (75L) — removed, use Rich defaults
- `keymap.py` (71L) — removed, no custom shortcuts
- `shortcuts_dialog.py` (71L) — removed
- `history.py` (66L) — replaced by `FileHistory`
- `commit_manager.py` (58L) — replaced by `print_final()`
- `pickers.py` (57L) — replaced by /commands
- `tool_key_args.py` (67L) — removed
- `data_models.py` (40L) — removed
- `layout.py` (34L) — removed
- `render.py` (129L) — removed (was already legacy)

### Features Removed

1. Adaptive refresh rate engine (5-20Hz)
2. 3-theme preset system (default/dark/high-contrast)
3. Session picker dialog (Ctrl+R)
4. Tree navigation picker (Ctrl+T)
5. Model cycle picker (Ctrl+L/P)
6. 8 keyboard shortcuts (Ctrl+R/T/L/P/N/K/Y/D)
7. Extension UI bridge (PtkExtensionUIContext)
8. Diff renderer (side-by-side)
9. Streaming syntax highlighter
10. Fuzzy completers (/ and @)
11. CommitManager scrollback system
12. StateManager (SSoT pattern)
13. Shortcuts help dialog
14. Entry limit buffer (240 entries)
15. Custom editor components
16. Extension command pool
17. ToolcallPreview streaming
18. Bottom toolbar status

## Migration

### Phase 1: Write New Code
1. Create `interactive/app.py` (~200L)
2. Create `interactive/stream_view.py` (~150L)
3. Update `interactive/__init__.py` (~50L)

### Phase 2: Update References
4. Update `modes/interactive_mode.py` imports
5. Update or stub any extension integration points

### Phase 3: Delete Old Code
6. Delete 19 old files from `interactive/`

### Phase 4: Tests
7. Rewrite 2 test files for new API
8. Delete 4 obsolete test files
9. Run full suite to verify

## Success Criteria

- Interactive UI is **3 files, ≤500 lines total**
- Streaming output works (text appears incrementally)
- Tool call status displays (running spinner, done ✓, error ✗)
- `/quit`, `/model`, `/resume`, `/help`, `/compact` commands work
- `Ctrl+C` interrupts current agent run
- Input history persists across sessions
- All existing tests pass (after rewrite)
- `extensions/ui.py` unchanged, no-op fallback works
