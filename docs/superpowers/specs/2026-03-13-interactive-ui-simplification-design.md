# Interactive UI Simplification Design

**Date:** 2026-03-13
**Status:** Draft
**Reference:** `/Users/looper/workspace/bub` (Bub project)

## Problem

The current interactive UI in `src/gen_agent/interactive/` consists of 22 files and 3,394 lines of code. It includes adaptive refresh rates, 3-layer state management, extension UI bridges, picker dialogs, streaming syntax highlighting, diff renderers, and 8 keyboard shortcuts. This complexity is disproportionate to the user-facing value it delivers.

The reference project Bub achieves a fully functional interactive CLI with 4 files and 428 lines, using the same technology stack (prompt_toolkit + Rich).

## Goal

Rewrite the interactive UI following Bub's minimal architecture pattern. Target: **3 files, ≤500 lines**. Retain streaming output and tool call display. Remove everything else.

## Design

### New File Structure

```
src/gen_agent/interactive/
├── app.py          (~200 lines)  — REPL loop + command dispatch + prompt input
├── stream_view.py  (~250 lines)  — Rich.Live streaming + event processing + tool display
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
        self._active_task: asyncio.Task | None = None

    async def run(self, initial_message: str | None = None) -> int:
        """Main REPL loop."""
        self._print_welcome()
        if initial_message:
            await self._run_agent(initial_message)
        with patch_stdout(raw=True):
            while True:
                try:
                    text = await self._prompt.prompt_async()
                except (EOFError, KeyboardInterrupt):
                    break
                text = text.strip()
                if not text:
                    continue
                # Delegate to session.prompt() which handles all slash commands
                # internally (/model, /resume, /compact, /session, etc.)
                # Only /quit and /help are handled locally.
                if text == "/quit":
                    break
                elif text == "/help":
                    self._print_help()
                else:
                    # session.prompt() handles both slash commands and agent prompts
                    await self._run_agent(text)
        return 0

    async def _run_agent(self, prompt: str):
        """Run agent with streaming display and SIGINT handling."""
        view = StreamView(self._console)
        unsub = self._session.subscribe(view.on_event)
        view.start()

        # Install SIGINT handler for cancel support
        loop = asyncio.get_running_loop()
        original_handler = signal.getsignal(signal.SIGINT)
        cancel_count = 0
        last_cancel = 0.0

        def _sigint_handler(sig, frame):
            nonlocal cancel_count, last_cancel
            now = time.monotonic()
            if now - last_cancel < 1.5:
                cancel_count += 1
            else:
                cancel_count = 1
            last_cancel = now
            if cancel_count >= 2:
                # Double Ctrl+C: force quit
                signal.signal(signal.SIGINT, original_handler)
                raise KeyboardInterrupt
            # Use call_soon_threadsafe to safely cancel from signal context
            if self._active_task and not self._active_task.done():
                loop.call_soon_threadsafe(self._active_task.cancel)

        try:
            signal.signal(signal.SIGINT, _sigint_handler)
            self._active_task = asyncio.create_task(
                self._session.prompt(prompt)
            )
            result = await self._active_task
            # session.prompt() returns messages for slash commands (e.g. /model).
            # Print any returned assistant messages as direct output.
            if result:
                for msg in result if isinstance(result, list) else [result]:
                    content = getattr(msg, "content", None) or str(msg)
                    if content:
                        self._console.print(content)
        except asyncio.CancelledError:
            self._console.print("[yellow]Interrupted.[/yellow]")
        except SystemExit:
            pass  # /quit handled by session raises SystemExit
        except Exception as exc:
            self._console.print(f"[red]Error: {exc}[/red]")
        finally:
            signal.signal(signal.SIGINT, original_handler)
            self._active_task = None
            view.stop()
            unsub()
            view.print_final(self._console)

    def _print_help(self):
        """Show common commands (session supports more via /commands)."""
        self._console.print(Panel(
            "Common commands:\n"
            "/quit     Exit the session\n"
            "/model    Switch model (e.g. /model gpt-4)\n"
            "/resume   Resume a session (e.g. /resume <id>)\n"
            "/compact  Trigger manual compaction\n"
            "/session  Show session info\n"
            "/help     Show this help\n"
            "\nShortcuts:\n"
            "Ctrl+C    Interrupt current agent run\n"
            "Ctrl+C×2  Force quit\n"
            "\nAll /commands are handled by the session. "
            "Type any /command to see if it's available.",
            title="Help",
            border_style="cyan",
        ))

    def _print_welcome(self):
        """Show startup banner."""
        provider = getattr(self._session, "provider_name", "")
        model = getattr(self._session, "model_id", "default")
        display = f"{provider}/{model}" if provider else model
        self._console.print(Panel(
            f"Model: {display}",
            title="gen-agent",
            border_style="cyan",
        ))

    def _build_prompt(self) -> PromptSession:
        """Create prompt_toolkit session with minimal config."""
        commands = ["/quit", "/model", "/resume", "/help", "/compact", "/session"]
        return PromptSession(
            message="> ",
            completer=WordCompleter(commands, sentence=True),
            history=FileHistory(str(self._history_path())),
        )

    def _history_path(self) -> Path:
        """History file per workspace, under config dir."""
        config_dir = Path.home() / ".config" / "gen-agent" / "user-history"
        config_dir.mkdir(parents=True, exist_ok=True)
        cwd_hash = hashlib.md5(str(Path.cwd()).encode()).hexdigest()[:12]
        return config_dir / f"{cwd_hash}.txt"
```

**Key decisions:**
- `PromptSession` with `WordCompleter` — no fuzzy matching, no @ path completion.
- `FileHistory` — reuse prompt_toolkit's built-in, no custom `HistoryStore`.
- `patch_stdout(raw=True)` — prevents Rich.Live and prompt_toolkit from corrupting each other.
- No custom keyboard shortcuts beyond Ctrl+C (handled by SIGINT handler).
- **Command routing**: Only `/quit` and `/help` handled locally. All other input (including slash commands like `/model`, `/resume`, `/compact`) delegated to `session.prompt()` which already implements them. This avoids duplicating session-level logic.
- **Slash command responses**: `session.prompt()` returns messages for slash commands. `_run_agent` captures the return value and prints any content, so commands like `/model` provide visible feedback.
- SIGINT handler: First Ctrl+C cancels `asyncio.Task` via `loop.call_soon_threadsafe()` (signal-safe), double Ctrl+C (within 1.5s) force-quits.
- **Error handling**: Catches `CancelledError` (interrupt), `SystemExit` (session /quit), and generic `Exception` (provider errors, network failures) to keep the REPL alive.
- `initial_message` passed to `run()` as parameter, not via private method.
- History stored at `~/.config/gen-agent/user-history/{cwd_hash}.txt`.

### stream_view.py — StreamView (~250 lines)

Merges: `live_view.py`, `event_processor.py`, `state_manager.py`, `render_engine.py`, `commit_manager.py`, `blocks.py`, `renderers.py`, `syntax_highlighter.py`, `diff_renderer.py`, `theme.py`, `data_models.py`, `tool_key_args.py`, `layout.py`, `render.py`.

```python
@dataclass
class ToolStatus:
    """Minimal tool call tracking."""
    name: str
    args_summary: str = ""
    status: Literal["running", "done", "error"] = "running"
    start_time: float = field(default_factory=time.monotonic)
    duration: float = 0.0
    is_error: bool = False

class StreamView:
    """Streams agent output via Rich.Live."""

    def __init__(self, console: Console):
        self._console = console
        self._live = Live(console=console, refresh_per_second=10, transient=True)
        self._text_parts: list[str] = []
        self._tools: dict[str, ToolStatus] = {}
        self._working = False
        self._error: str | None = None
        self._notice: str | None = None

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
                self._notice = None
            case "message_update":
                self._on_message_update(event)
            case "tool_execution_start":
                # Event attributes are directly on the event object
                self._tools[event.tool_call_id] = ToolStatus(
                    name=event.tool_name,
                    args_summary=_summarize_args(event.args),
                )
            case "tool_execution_end":
                ts = self._tools.get(event.tool_call_id)
                if ts:
                    ts.status = "error" if event.is_error else "done"
                    ts.duration = time.monotonic() - ts.start_time
                    ts.is_error = event.is_error
            case "agent_end":
                self._working = False
            case "auto_compaction_start":
                self._notice = "Compacting context..."
            case "auto_compaction_end":
                self._notice = None
            case "auto_retry_start":
                self._notice = "Retrying..."
            case "auto_retry_end":
                self._notice = None
            # Ignore other event types gracefully
        self._refresh()

    def _on_message_update(self, event):
        """Handle streaming text deltas."""
        msg = event.assistant_message_event
        match msg.type:
            case "text_delta":
                self._text_parts.append(msg.delta)
            case "error":
                self._error = msg.error
            # Ignore thinking_delta, toolcall_delta, etc.

    def _refresh(self):
        """Build renderable group and update Live."""
        parts = []
        text = "".join(self._text_parts)
        if text:
            parts.append(Markdown(text))
        for ts in self._tools.values():
            parts.append(self._render_tool(ts))
        if self._notice:
            parts.append(Text(f"  {self._notice}", style="dim"))
        if self._error:
            parts.append(Text(f"  Error: {self._error}", style="red"))
        if self._working and not self._notice:
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
        """Print completed output to scrollback (Live was transient)."""
        text = "".join(self._text_parts)
        if text:
            console.print(Markdown(text))
        for ts in self._tools.values():
            console.print(self._render_tool(ts))


def _summarize_args(args: dict[str, Any]) -> str:
    """Extract a short summary from tool call arguments."""
    # Prioritize common keys that identify the action target
    for key in ("path", "file_path", "command", "url", "query", "name"):
        if key in args:
            val = str(args[key])
            return val[:60] + "..." if len(val) > 60 else val
    # Fallback: first string value
    for val in args.values():
        if isinstance(val, str) and val:
            return val[:40] + "..." if len(val) > 40 else val
    return ""
```

**Key decisions:**
- State is instance variables: `_text_parts`, `_tools`, `_working`, `_notice`, `_error`. No separate StateManager.
- No adaptive refresh — `Rich.Live(refresh_per_second=10)` handles rate limiting.
- **`transient=True`** — Live content clears on stop. `print_final()` then outputs the permanent copy to scrollback. This avoids double-rendering.
- No streaming syntax highlighter — `Rich.Markdown` uses Pygments internally.
- No diff renderer — tool results shown as status lines only.
- No theme system — use Rich's default styles directly.
- `ToolStatus.start_time` captured at creation; `duration` computed as delta on end.
- `_summarize_args()` — simple key-priority heuristic, ~15 lines. Replaces `extract_tool_key_arg` (67L).
- Handles `auto_compaction_*` and `auto_retry_*` events as transient notices.
- Unknown event types are silently ignored (forward-compatible).

### __init__.py — Public API (~50 lines)

```python
import sys
from rich.console import Console
from .app import InteractiveApp
from .stream_view import StreamView

async def run_interactive_mode(session, initial_message=None, console=None):
    """Entry point for interactive mode.

    Falls back to print mode when stdin/stdout are not TTYs.
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        from gen_agent.modes.print_mode import run_print_mode
        return await run_print_mode(session, initial_message)

    console = console or Console()
    app = InteractiveApp(session, console)
    return await app.run(initial_message=initial_message)

__all__ = ["InteractiveApp", "StreamView", "run_interactive_mode"]
```

**Key decision:** TTY guard preserved — non-interactive invocations fall back to print mode, matching current behavior.

### Extension UI Impact

`extensions/ui.py` defines `ExtensionUIContext` protocol and `NoOpExtensionUIContext`. These stay **unchanged**. The current interactive mode's `PtkExtensionUIContext` implementation is deleted — extensions will use the no-op fallback. No adapter code needed.

### External References to Update

| File | Current Import | Change |
|------|---------------|--------|
| `modes/interactive_mode.py` | `from gen_agent.interactive.ptk_app import ...` | Update to `from gen_agent.interactive import InteractiveApp, run_interactive_mode` |
| `modes/interactive_mode.py` | `from gen_agent.interactive.blocks import LIVE_CHAR_LIMIT` | Remove (no longer needed) |
| `tests/unit/test_interactive_live_view.py` | `from gen_agent.interactive.blocks import ...` | Rewrite for `StreamView` |
| `tests/unit/test_interactive_mode.py` | `from gen_agent.interactive.ptk_app import ...` | Rewrite for `InteractiveApp` |
| `tests/unit/test_interactive_history.py` | `from gen_agent.interactive.history import ...` | Delete file |
| `tests/unit/test_interactive_prompt_session.py` | `from gen_agent.interactive.prompt_session import ...` | Delete file |
| `tests/unit/test_interactive_completers.py` | `from gen_agent.interactive.completers import ...` | Delete file |
| `tests/unit/test_interactive_reducers.py` | `from gen_agent.interactive.render import ...` | Delete file |
| `tests/integration/test_interactive_flow.py` | `from gen_agent.interactive.blocks import ...` | Rewrite for new API |

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

### Files Deleted (21 of 22, `__init__.py` rewritten in place)

**Replaced** (code rewritten in new files):
- `ptk_app.py` (412L) → `app.py`
- `live_view.py` (532L) → `stream_view.py`
- `event_processor.py` (396L) → inlined into `stream_view.py`

**Removed entirely** (functionality no longer needed):
- `state_manager.py` (187L) — state is instance vars on `StreamView`
- `render_engine.py` (184L) — `Rich.Live` handles refresh
- `blocks.py` (279L) — replaced by `ToolStatus` dataclass
- `renderers.py` (129L) — inlined into `stream_view.py`
- `prompt_session.py` (117L) — inlined into `app.py`
- `completers.py` (167L) — replaced by `WordCompleter`
- `diff_renderer.py` (151L)
- `syntax_highlighter.py` (144L) — `Rich.Markdown` handles this
- `theme.py` (75L) — use Rich defaults
- `keymap.py` (71L) — no custom shortcuts
- `shortcuts_dialog.py` (71L)
- `history.py` (66L) — replaced by `FileHistory`
- `commit_manager.py` (58L) — replaced by `print_final()`
- `pickers.py` (57L) — replaced by session.prompt() commands
- `tool_key_args.py` (67L) — replaced by `_summarize_args()`
- `data_models.py` (40L)
- `layout.py` (34L)
- `render.py` (129L) — was already legacy

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
2. Create `interactive/stream_view.py` (~250L)
3. Update `interactive/__init__.py` (~50L)

### Phase 2: Update References
4. Update `modes/interactive_mode.py` imports
5. Verify `extensions/ui.py` no-op fallback is wired correctly

### Phase 3: Delete Old Code
6. Delete 19 old files from `interactive/`

### Phase 4: Tests
7. Rewrite 2 test files for new API (`test_interactive_live_view.py`, `test_interactive_mode.py`)
8. Rewrite 1 integration test (`test_interactive_flow.py`)
9. Delete 4 obsolete test files
10. Run full suite to verify

## Success Criteria

- Interactive UI is **3 files, ≤500 lines total**
- Streaming output works (text appears incrementally)
- Tool call status displays (running spinner, done ✓, error ✗)
- Slash commands work via `session.prompt()` delegation
- `Ctrl+C` interrupts current agent run (double Ctrl+C force-quits)
- Input history persists across sessions
- TTY guard falls back to print mode for non-interactive use
- `patch_stdout` prevents terminal corruption
- All existing tests pass (after rewrite)
- `extensions/ui.py` unchanged, no-op fallback works
