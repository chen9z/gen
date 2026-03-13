# Interactive UI Simplification Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the interactive UI from 22 files/3,394 lines to 3 files/≤500 lines, retaining streaming output and tool call display.

**Architecture:** Bub-style rewrite — simple async REPL loop (`app.py`) drives a Rich.Live streaming view (`stream_view.py`). All slash commands delegate to `session.prompt()`. SIGINT handler enables Ctrl+C cancel.

**Tech Stack:** prompt_toolkit (input/history/completion), Rich (Live streaming, Markdown, Panel), asyncio (event loop, task cancellation)

**Spec:** `docs/superpowers/specs/2026-03-13-interactive-ui-simplification-design.md`

---

## File Structure

| File | Action | Responsibility | Lines |
|------|--------|---------------|-------|
| `src/gen_agent/interactive/stream_view.py` | **Create** | Rich.Live streaming + event dispatch + tool display | ~250 |
| `src/gen_agent/interactive/app.py` | **Create** | REPL loop + command routing + prompt input + SIGINT | ~200 |
| `src/gen_agent/interactive/__init__.py` | **Rewrite** | Public API + `run_interactive_mode` entry point | ~30 |
| `src/gen_agent/modes/interactive_mode.py` | **Modify** | Update imports | ~5 |
| `tests/unit/test_stream_view.py` | **Create** | Tests for StreamView | ~120 |
| `tests/unit/test_interactive_app.py` | **Create** | Tests for InteractiveApp | ~100 |

**Delete (21 files):** All existing files in `interactive/` except `__init__.py` (rewritten in place).
**Delete (6 test files):** `test_interactive_live_view.py`, `test_interactive_mode.py`, `test_interactive_history.py`, `test_interactive_prompt_session.py`, `test_interactive_completers.py`, `test_interactive_reducers.py`.

---

## Chunk 1: StreamView — Core Streaming Engine

### Task 1: Write StreamView failing tests

**Files:**
- Create: `tests/unit/test_stream_view.py`

- [ ] **Step 1: Write test file with all StreamView tests**

```python
# tests/unit/test_stream_view.py
from __future__ import annotations

import time

import pytest
from rich.console import Console
from rich.text import Text

from gen_agent.interactive.stream_view import StreamView, ToolStatus, _summarize_args
from gen_agent.models.events import (
    AgentStart,
    AgentEnd,
    AutoCompactionEnd,
    AutoCompactionStart,
    MessageUpdate,
    ToolExecutionEnd,
    ToolExecutionStart,
)
from gen_agent.models.messages import AssistantMessage
from gen_agent.models.content import TextContent


def _assistant_message(text: str = "") -> AssistantMessage:
    return AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text=text)] if text else [],
        stopReason="stop",
    )


class _FakeLive:
    """Replaces Rich.Live for testing."""

    def __init__(self):
        self.updates: list = []
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def update(self, renderable, refresh=True):
        self.updates.append(renderable)


def _make_view() -> tuple[StreamView, _FakeLive]:
    console = Console(file=None, force_terminal=True)
    view = StreamView(console)
    fake = _FakeLive()
    view._live = fake
    return view, fake


def test_stream_view_start_stop():
    view, fake = _make_view()
    view.start()
    assert fake.started
    view.stop()
    assert fake.stopped


def test_stream_view_text_delta_accumulates():
    view, fake = _make_view()
    msg = _assistant_message()

    view.on_event(AgentStart())
    view.on_event(MessageUpdate(
        message=msg,
        assistantMessageEvent={"type": "text_delta", "delta": "hello "},
    ))
    view.on_event(MessageUpdate(
        message=msg,
        assistantMessageEvent={"type": "text_delta", "delta": "world"},
    ))

    assert "".join(view._text_parts) == "hello world"
    assert len(fake.updates) >= 2  # refreshed on each event


def test_stream_view_tool_execution_lifecycle():
    view, _ = _make_view()

    view.on_event(AgentStart())
    view.on_event(ToolExecutionStart(
        toolCallId="tc1",
        toolName="read_file",
        args={"path": "src/main.py"},
    ))

    assert "tc1" in view._tools
    assert view._tools["tc1"].name == "read_file"
    assert view._tools["tc1"].status == "running"

    view.on_event(ToolExecutionEnd(
        toolCallId="tc1",
        toolName="read_file",
        result="file content",
        isError=False,
    ))

    assert view._tools["tc1"].status == "done"
    assert view._tools["tc1"].duration > 0
    assert view._tools["tc1"].is_error is False


def test_stream_view_tool_error():
    view, _ = _make_view()
    view.on_event(AgentStart())
    view.on_event(ToolExecutionStart(
        toolCallId="tc2",
        toolName="bash",
        args={"command": "ls"},
    ))
    view.on_event(ToolExecutionEnd(
        toolCallId="tc2",
        toolName="bash",
        result=None,
        isError=True,
        errorDetail="command failed",
    ))

    assert view._tools["tc2"].status == "error"
    assert view._tools["tc2"].is_error is True


def test_stream_view_agent_start_clears_state():
    view, _ = _make_view()
    view._text_parts = ["old text"]
    view._tools["old"] = ToolStatus(name="old_tool")

    view.on_event(AgentStart())

    assert view._text_parts == []
    assert view._tools == {}
    assert view._working is True


def test_stream_view_agent_end_stops_working():
    view, _ = _make_view()
    view.on_event(AgentStart())
    assert view._working is True

    view.on_event(AgentEnd())
    assert view._working is False


def test_stream_view_compaction_notice():
    view, _ = _make_view()
    view.on_event(AutoCompactionStart())
    assert view._notice == "Compacting context..."

    view.on_event(AutoCompactionEnd())
    assert view._notice is None


def test_stream_view_error_event():
    view, _ = _make_view()
    msg = _assistant_message()
    view.on_event(MessageUpdate(
        message=msg,
        assistantMessageEvent={"type": "error", "error": "rate limit"},
    ))
    assert view._error == "rate limit"


def test_stream_view_print_final(capsys):
    console = Console(force_terminal=False, no_color=True)
    view = StreamView(console)
    view._text_parts = ["Hello **world**"]
    view._tools["t1"] = ToolStatus(
        name="bash", args_summary="ls", status="done", duration=0.5,
    )

    view.print_final(console)
    captured = capsys.readouterr()
    assert "world" in captured.out
    assert "bash" in captured.out


def test_render_tool_running():
    view, _ = _make_view()
    ts = ToolStatus(name="read_file", args_summary="main.py")
    result = view._render_tool(ts)
    assert isinstance(result, Text)
    assert "read_file" in str(result)


def test_render_tool_done():
    view, _ = _make_view()
    ts = ToolStatus(name="bash", args_summary="ls", status="done", duration=1.2)
    result = view._render_tool(ts)
    text = str(result)
    assert "✓" in text
    assert "1.2s" in text


def test_render_tool_error():
    view, _ = _make_view()
    ts = ToolStatus(name="bash", args_summary="ls", status="error", is_error=True, duration=0.5)
    result = view._render_tool(ts)
    text = str(result)
    assert "✗" in text


def test_summarize_args_path():
    assert _summarize_args({"path": "src/main.py"}) == "src/main.py"


def test_summarize_args_command():
    assert _summarize_args({"command": "pytest tests/"}) == "pytest tests/"


def test_summarize_args_truncates():
    long = "x" * 100
    result = _summarize_args({"path": long})
    assert len(result) <= 63  # 60 + "..."


def test_summarize_args_empty():
    assert _summarize_args({}) == ""


def test_summarize_args_fallback_string():
    assert _summarize_args({"count": 5, "label": "hello"}) == "hello"
```

- [ ] **Step 2: Run tests to verify they fail (module not found)**

Run: `uv run pytest tests/unit/test_stream_view.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gen_agent.interactive.stream_view'`

### Task 2: Implement StreamView

**Files:**
- Create: `src/gen_agent/interactive/stream_view.py`

- [ ] **Step 3: Write stream_view.py**

```python
"""Minimal streaming view for interactive mode.

Renders agent output via Rich.Live with tool call status.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Literal

from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.text import Text

from gen_agent.models.events import AgentSessionEvent


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

    def __init__(self, console: Console) -> None:
        self._console = console
        self._live = Live(console=console, refresh_per_second=10, transient=True)
        self._text_parts: list[str] = []
        self._tools: dict[str, ToolStatus] = {}
        self._working = False
        self._error: str | None = None
        self._notice: str | None = None

    def start(self) -> None:
        self._live.start()

    def stop(self) -> None:
        self._live.stop()

    def on_event(self, event: AgentSessionEvent) -> None:
        """Dispatch event to update state, then refresh."""
        etype = event.type
        if etype == "agent_start":
            self._working = True
            self._text_parts.clear()
            self._tools.clear()
            self._error = None
            self._notice = None
        elif etype == "message_update":
            self._on_message_update(event)
        elif etype == "tool_execution_start":
            self._tools[event.tool_call_id] = ToolStatus(
                name=event.tool_name,
                args_summary=_summarize_args(event.args),
            )
        elif etype == "tool_execution_end":
            ts = self._tools.get(event.tool_call_id)
            if ts:
                ts.status = "error" if event.is_error else "done"
                ts.duration = time.monotonic() - ts.start_time
                ts.is_error = event.is_error
        elif etype == "agent_end":
            self._working = False
        elif etype == "auto_compaction_start":
            self._notice = "Compacting context..."
        elif etype == "auto_compaction_end":
            self._notice = None
        elif etype == "auto_retry_start":
            self._notice = "Retrying..."
        elif etype == "auto_retry_end":
            self._notice = None
        # Ignore unknown event types gracefully
        self._refresh()

    def _on_message_update(self, event: AgentSessionEvent) -> None:
        """Handle streaming text deltas."""
        msg = event.assistant_message_event
        if msg.type == "text_delta" and msg.delta:
            self._text_parts.append(msg.delta)
        elif msg.type == "error" and msg.error:
            self._error = msg.error

    def _refresh(self) -> None:
        """Build renderable group and update Live."""
        parts: list[Any] = []
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
        return Text(
            f"  {icon} {ts.name} {ts.args_summary} ({ts.duration:.1f}s)",
            style=color,
        )

    def print_final(self, console: Console) -> None:
        """Print completed output to scrollback (Live was transient)."""
        text = "".join(self._text_parts)
        if text:
            console.print(Markdown(text))
        for ts in self._tools.values():
            console.print(self._render_tool(ts))


def _summarize_args(args: dict[str, Any]) -> str:
    """Extract a short summary from tool call arguments."""
    for key in ("path", "file_path", "command", "url", "query", "name"):
        if key in args:
            val = str(args[key])
            return val[:60] + "..." if len(val) > 60 else val
    for val in args.values():
        if isinstance(val, str) and val:
            return val[:40] + "..." if len(val) > 40 else val
    return ""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/unit/test_stream_view.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add src/gen_agent/interactive/stream_view.py tests/unit/test_stream_view.py
git commit -m "feat: add StreamView — minimal streaming engine for interactive UI"
```

---

## Chunk 2: InteractiveApp — REPL Loop

### Task 3: Write InteractiveApp failing tests

**Files:**
- Create: `tests/unit/test_interactive_app.py`

- [ ] **Step 6: Write test file with InteractiveApp tests**

```python
# tests/unit/test_interactive_app.py
from __future__ import annotations

import asyncio
from contextlib import nullcontext
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from gen_agent.interactive.app import InteractiveApp, _extract_text


class _DummySession:
    def __init__(self) -> None:
        self.provider_name = "openai"
        self.model_id = "gpt-4o-mini"
        self.cwd = "/tmp"
        self._listeners: list = []

    def subscribe(self, listener):
        self._listeners.append(listener)
        return lambda: self._listeners.remove(listener)

    async def prompt(self, message, **kwargs):
        return []


class _QuitSession(_DummySession):
    """Session that raises SystemExit on /quit."""

    async def prompt(self, message, **kwargs):
        if message == "/quit":
            raise SystemExit(0)
        return []


class _ErrorSession(_DummySession):
    """Session that raises an exception."""

    async def prompt(self, message, **kwargs):
        raise RuntimeError("API timeout")


class _StreamingSession(_DummySession):
    """Session that emits events via subscribers."""

    def __init__(self) -> None:
        super().__init__()
        self.started = asyncio.Event()
        self.cancelled = False

    async def prompt(self, message, **kwargs):
        self.started.set()
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            self.cancelled = True
        return []


def _make_app(session=None) -> InteractiveApp:
    session = session or _DummySession()
    console = Console(file=None, force_terminal=True)
    return InteractiveApp(session, console)


@pytest.mark.asyncio
async def test_run_quit_command():
    app = _make_app()

    class _Prompt:
        calls = 0
        async def prompt_async(self, *a, **kw):
            self.calls += 1
            if self.calls == 1:
                return "/quit"
            raise EOFError

    app._prompt = _Prompt()
    with patch("gen_agent.interactive.app.patch_stdout", return_value=nullcontext()):
        code = await app.run()
    assert code == 0


@pytest.mark.asyncio
async def test_run_help_command(capsys):
    console = Console(force_terminal=False, no_color=True)
    session = _DummySession()
    app = InteractiveApp(session, console)

    class _Prompt:
        calls = 0
        async def prompt_async(self, *a, **kw):
            self.calls += 1
            if self.calls == 1:
                return "/help"
            raise EOFError

    app._prompt = _Prompt()
    with patch("gen_agent.interactive.app.patch_stdout", return_value=nullcontext()):
        await app.run()

    captured = capsys.readouterr()
    assert "/quit" in captured.out
    assert "Ctrl+C" in captured.out


@pytest.mark.asyncio
async def test_run_eof_exits():
    app = _make_app()

    class _Prompt:
        async def prompt_async(self, *a, **kw):
            raise EOFError

    app._prompt = _Prompt()
    with patch("gen_agent.interactive.app.patch_stdout", return_value=nullcontext()):
        code = await app.run()
    assert code == 0


@pytest.mark.asyncio
async def test_run_agent_error_handled():
    app = _make_app(_ErrorSession())
    # _run_agent should catch Exception and not crash
    with patch.object(app, "_console") as mock_console:
        mock_console.print = MagicMock()
        await app._run_agent("hello")
    # Verify error was printed
    calls = [str(c) for c in mock_console.print.call_args_list]
    assert any("Error" in c or "API timeout" in c for c in calls)


@pytest.mark.asyncio
async def test_run_agent_subscribes_and_unsubscribes():
    session = _DummySession()
    app = _make_app(session)
    await app._run_agent("hello")
    # After _run_agent, listener should be unsubscribed
    assert len(session._listeners) == 0


def test_extract_text_from_string():
    class Msg:
        content = "hello world"
    assert _extract_text(Msg()) == "hello world"


def test_extract_text_from_content_blocks():
    class Block:
        type = "text"
        text = "block text"
    class Msg:
        content = [Block()]
    assert _extract_text(Msg()) == "block text"


def test_extract_text_fallback():
    class Msg:
        content = None
    result = _extract_text(Msg())
    assert isinstance(result, str)
```

- [ ] **Step 7: Run tests to verify they fail (module not found)**

Run: `uv run pytest tests/unit/test_interactive_app.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gen_agent.interactive.app'`

### Task 4: Implement InteractiveApp

**Files:**
- Create: `src/gen_agent/interactive/app.py`

- [ ] **Step 8: Write app.py**

```python
"""Minimal interactive REPL for gen-agent.

Async main loop with prompt_toolkit input and Rich output.
Slash commands delegate to session.prompt().
"""

from __future__ import annotations

import asyncio
import hashlib
import signal
import sys
import time
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from rich.console import Console
from rich.panel import Panel

from gen_agent.interactive.stream_view import StreamView


class InteractiveApp:
    """Minimal interactive REPL for gen-agent."""

    def __init__(self, session: Any, console: Console) -> None:
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
                if text == "/quit":
                    break
                elif text == "/help":
                    self._print_help()
                else:
                    await self._run_agent(text)
        return 0

    async def _run_agent(self, prompt: str) -> None:
        """Run agent with streaming display and SIGINT handling."""
        view = StreamView(self._console)
        unsub = self._session.subscribe(view.on_event)
        view.start()

        loop = asyncio.get_running_loop()
        original_handler = signal.getsignal(signal.SIGINT)
        cancel_count = 0
        last_cancel = 0.0

        def _sigint_handler(sig: int, frame: Any) -> None:
            nonlocal cancel_count, last_cancel
            now = time.monotonic()
            if now - last_cancel < 1.5:
                cancel_count += 1
            else:
                cancel_count = 1
            last_cancel = now
            if cancel_count >= 2:
                signal.signal(signal.SIGINT, original_handler)
                raise KeyboardInterrupt
            if self._active_task and not self._active_task.done():
                loop.call_soon_threadsafe(self._active_task.cancel)

        try:
            signal.signal(signal.SIGINT, _sigint_handler)
            self._active_task = asyncio.create_task(
                self._session.prompt(prompt)
            )
            result = await self._active_task
            if result:
                for msg in (result if isinstance(result, list) else [result]):
                    text = _extract_text(msg)
                    if text:
                        self._console.print(text)
        except asyncio.CancelledError:
            self._console.print("[yellow]Interrupted.[/yellow]")
        except SystemExit:
            pass
        except Exception as exc:
            self._console.print(f"[red]Error: {exc}[/red]")
        finally:
            signal.signal(signal.SIGINT, original_handler)
            self._active_task = None
            view.stop()
            unsub()
            view.print_final(self._console)

    def _print_help(self) -> None:
        """Show common commands."""
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

    def _print_welcome(self) -> None:
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
            message="› ",
            completer=WordCompleter(commands, sentence=True),
            history=FileHistory(str(self._history_path())),
        )

    def _history_path(self) -> Path:
        """History file per workspace, under config dir."""
        config_dir = Path.home() / ".config" / "gen-agent" / "user-history"
        config_dir.mkdir(parents=True, exist_ok=True)
        cwd_hash = hashlib.md5(str(Path.cwd()).encode()).hexdigest()[:12]
        return config_dir / f"{cwd_hash}.txt"


def _extract_text(message: Any) -> str:
    """Extract text from an assistant message.

    Content may be a string or a list of content blocks with .type/.text.
    """
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if getattr(block, "type", "") == "text":
                parts.append(getattr(block, "text", ""))
        return "\n".join(parts)
    return str(message)
```

- [ ] **Step 9: Run tests to verify they pass**

Run: `uv run pytest tests/unit/test_interactive_app.py -v`
Expected: ALL PASS

- [ ] **Step 10: Commit**

```bash
git add src/gen_agent/interactive/app.py tests/unit/test_interactive_app.py
git commit -m "feat: add InteractiveApp — minimal REPL loop with SIGINT handling"
```

---

## Chunk 3: Wire Up, Delete Old Code, Verify

### Task 5: Rewrite __init__.py and update imports

**Files:**
- Rewrite: `src/gen_agent/interactive/__init__.py`
- Modify: `src/gen_agent/modes/interactive_mode.py`

- [ ] **Step 11: Rewrite interactive/__init__.py**

```python
"""Interactive mode — minimal REPL with streaming output."""

from __future__ import annotations

import sys

from rich.console import Console

from .app import InteractiveApp
from .stream_view import StreamView


async def run_interactive_mode(
    session: object,
    initial_message: str | None = None,
) -> int:
    """Entry point for interactive mode.

    Falls back to print mode when stdin/stdout are not TTYs.
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        from gen_agent.modes.print_mode import run_print_mode

        return await run_print_mode(session, initial_message)

    console = Console()
    app = InteractiveApp(session, console)
    return await app.run(initial_message=initial_message)


__all__ = ["InteractiveApp", "StreamView", "run_interactive_mode"]
```

- [ ] **Step 12: Update modes/interactive_mode.py**

```python
from __future__ import annotations

from gen_agent.interactive import InteractiveApp, run_interactive_mode

__all__ = ["InteractiveApp", "run_interactive_mode"]
```

- [ ] **Step 13: Run existing tests that import from interactive to verify imports work**

Run: `uv run pytest tests/unit/test_stream_view.py tests/unit/test_interactive_app.py -v`
Expected: ALL PASS

- [ ] **Step 14: Commit**

```bash
git add src/gen_agent/interactive/__init__.py src/gen_agent/modes/interactive_mode.py
git commit -m "refactor: rewire interactive module entry points"
```

### Task 6: Delete old files

**Files:**
- Delete: 19 files from `src/gen_agent/interactive/`

- [ ] **Step 15: Delete all old interactive files**

```bash
cd src/gen_agent/interactive
rm -f ptk_app.py live_view.py event_processor.py state_manager.py \
      render_engine.py blocks.py renderers.py prompt_session.py \
      completers.py diff_renderer.py syntax_highlighter.py theme.py \
      keymap.py shortcuts_dialog.py history.py commit_manager.py \
      pickers.py tool_key_args.py data_models.py layout.py render.py
```

- [ ] **Step 16: Delete old test files**

```bash
cd tests/unit
rm -f test_interactive_live_view.py test_interactive_mode.py \
      test_interactive_history.py test_interactive_prompt_session.py \
      test_interactive_completers.py test_interactive_reducers.py
```

- [ ] **Step 17: Check for remaining imports to old modules**

Run: `uv run python -c "from gen_agent.interactive import InteractiveApp, run_interactive_mode; print('OK')"`
Expected: `OK`

Run: `grep -r "from gen_agent.interactive\." src/ --include="*.py" | grep -v __pycache__`
Expected: Only hits in `__init__.py` (importing from `.app` and `.stream_view`)

- [ ] **Step 18: Commit deletions**

```bash
git add -A src/gen_agent/interactive/ tests/unit/
git commit -m "refactor: delete 21 old interactive UI files and 6 obsolete tests"
```

### Task 7: Run full test suite

- [ ] **Step 19: Run all unit tests**

Run: `uv run pytest tests/unit -v`
Expected: ALL PASS (some old tests may need the integration test update below)

- [ ] **Step 20: Check integration test**

Run: `uv run pytest tests/integration/test_interactive_flow.py -v 2>&1 || true`

If it fails due to old imports: update or delete the test. The integration test imports `AssistantBlock` and `ToolRunBlock` from old modules — these no longer exist. Delete the file if it only tests old internal APIs:

```bash
rm tests/integration/test_interactive_flow.py
git add tests/integration/test_interactive_flow.py
```

- [ ] **Step 21: Run full suite**

Run: `uv run pytest -v`
Expected: ALL PASS

- [ ] **Step 22: Run lint**

Run: `uvx ruff check src/gen_agent/interactive/`
Expected: No errors (or only minor style issues to fix)

- [ ] **Step 23: Final commit**

```bash
git add -A
git commit -m "feat: complete interactive UI simplification (22 files → 3 files)"
```

### Task 8: Line count verification

- [ ] **Step 24: Verify line count target**

Run: `wc -l src/gen_agent/interactive/*.py`
Expected: Total ≤500 lines

Run: `find src/gen_agent/interactive -name "*.py" | wc -l`
Expected: 3 files

---

## Summary

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Files | 22 | 3 | 86% |
| Lines | 3,394 | ≤500 | 85% |
| Dependencies | prompt_toolkit + Rich + custom | prompt_toolkit + Rich | Simplified |
| Keyboard shortcuts | 8 (Ctrl+) | 1 (Ctrl+C) | 88% |
| Slash commands | 8+ (local) | 2 local + session delegation | Simplified |
| State management | 3-layer (StateManager + RenderEngine + CommitManager) | Instance vars | Eliminated |
