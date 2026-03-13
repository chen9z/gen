# Interactive UI/Rendering Optimization — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rework interactive mode's rendering to match Claude Code's UI patterns — collapsible thinking, compact tool display, icon-prefixed notices, cleaned-up dead code.

**Architecture:** Keep existing LiveView + EventProcessor + blocks pipeline. Changes target block `render()` methods, notice formatting in LiveView, and dead code removal. No new abstractions.

**Tech Stack:** Rich (Console, Text, Markdown, Spinner, Group, Layout), Python 3.11+

---

### Task 1: Delete dead code (theme.py, layout.py, RenderEngine dead methods)

**Files:**
- Delete: `src/gen_agent/interactive/theme.py`
- Delete: `src/gen_agent/interactive/layout.py`
- Modify: `src/gen_agent/interactive/__init__.py`
- Modify: `src/gen_agent/interactive/render_engine.py:57-135`
- Modify: `src/gen_agent/interactive/blocks.py:263-271` (NoticeBlock)

**Step 1: Delete theme.py and layout.py**

```bash
rm src/gen_agent/interactive/theme.py src/gen_agent/interactive/layout.py
```

**Step 2: Update __init__.py — remove theme/layout imports**

Replace entire `src/gen_agent/interactive/__init__.py` with:

```python
from .ptk_app import GenInteractiveApp, LIVE_CHAR_LIMIT, PtkExtensionUIContext, run_interactive_mode
from .event_processor import EventProcessor
from .render_engine import RenderEngine

__all__ = [
    "GenInteractiveApp",
    "LIVE_CHAR_LIMIT",
    "PtkExtensionUIContext",
    "run_interactive_mode",
    "EventProcessor",
    "RenderEngine",
]
```

**Step 3: Remove dead methods from render_engine.py**

Delete `build_renderable()` (lines 57-115) and `_flush_loop()` (lines 122-135). Also remove unused imports `Group`, `Layout`, `Text`, `AssistantBlock`, `ToolRunBlock`. The file should contain only:

```python
from __future__ import annotations

import asyncio
import time

from rich.console import Console, RenderableType
from rich.live import Live


class RenderEngine:
    """Manages Rich Live instance lifecycle and flush."""

    def __init__(self, console: Console, batch_interval: float = 0.04):
        self._console = console
        self._batch_interval = batch_interval
        self._live: Live | None = None
        self._flush_task: asyncio.Task[None] | None = None
        self._dirty = True
        self._last_activity_time = time.monotonic()
        self._min_interval = 0.05
        self._max_interval = 0.2

    @property
    def console(self) -> Console:
        return self._console

    def start(self) -> None:
        if self._live is not None:
            return
        self._live = Live(
            console=self._console,
            auto_refresh=False,
            transient=True,
            vertical_overflow="visible",
            redirect_stdout=False,
            redirect_stderr=False,
        )
        self._live.start()

    def stop(self) -> None:
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None
        if self._live:
            self._live.stop()
            self._live = None

    def request_refresh(self) -> None:
        self._dirty = True
        self._last_activity_time = time.monotonic()

    def flush(self, renderable: RenderableType) -> None:
        if self._live is not None:
            self._live.update(renderable, refresh=True)
            self._dirty = False
```

**Step 4: Delete NoticeBlock from blocks.py**

Remove lines 263-271 (the `NoticeBlock` class) from `src/gen_agent/interactive/blocks.py`.

**Step 5: Run lint and tests**

```bash
uvx ruff check src/gen_agent/interactive/
uv run pytest tests/unit/test_interactive_live_view.py tests/unit/test_interactive_mode.py -v
```

Expected: All pass, no lint errors.

**Step 6: Commit**

```bash
git add -A src/gen_agent/interactive/
git commit -m "refactor: remove dead code (theme, layout, NoticeBlock, RenderEngine dead methods)"
```

---

### Task 2: Rework tool_key_args — basename for paths, shorter truncation

**Files:**
- Modify: `src/gen_agent/interactive/tool_key_args.py:43-54`

**Step 1: Update extract_tool_key_arg**

In `src/gen_agent/interactive/tool_key_args.py`, replace `extract_tool_key_arg` (lines 43-54) with:

```python
def _shorten_path(path: str, limit: int = 40) -> str:
    """Show basename, or tail of path if longer than limit."""
    if len(path) <= limit:
        return path
    import os
    base = os.path.basename(path)
    if len(base) <= limit:
        return base
    return base[:limit - 3] + "..."


def extract_tool_key_arg(name: str, args: dict[str, Any]) -> str:
    """Extract the most relevant argument for display."""
    normalized = normalize_tool_name(name)
    keys = TOOL_KEY_ARGS.get(normalized, [])
    for key in keys:
        value = args.get(key)
        if isinstance(value, str) and value.strip():
            if key in ("path", "file_path"):
                return _shorten_path(value)
            return value[:40] + "..." if len(value) > 40 else value
    for value in args.values():
        if isinstance(value, str) and value.strip():
            return value[:40] + "..." if len(value) > 40 else value
    return ""
```

**Step 2: Run lint and tests**

```bash
uvx ruff check src/gen_agent/interactive/tool_key_args.py
uv run pytest tests/unit -q
```

Expected: All pass.

**Step 3: Commit**

```bash
git add src/gen_agent/interactive/tool_key_args.py
git commit -m "refactor: shorten tool key_arg display (basename for paths, 40 char limit)"
```

---

### Task 3: Rework AssistantBlock.render() — collapsible thinking

**Files:**
- Modify: `src/gen_agent/interactive/blocks.py:39-148`

**Step 1: Add _show_thinking field and toggle method**

In the `AssistantBlock` dataclass, add after `_cached_render` (line 49):

```python
    _show_thinking: bool = field(default=False, init=False)
```

Add method after `finish()`:

```python
    def toggle_thinking(self) -> None:
        self._show_thinking = not self._show_thinking
        self._cached_render = None  # invalidate cache
```

**Step 2: Rewrite render() method**

Replace the entire `render()` method (lines 101-148) with:

```python
    def render(self) -> RenderableType:
        if self.done and self._cached_render is not None:
            return self._cached_render

        parts: list[RenderableType] = []

        # Thinking display
        if self.thinking:
            if not self.done and not self.text:
                # Still thinking, no text yet — spinner
                parts.append(Spinner("dots", text="Thinking...", style="dim italic"))
            else:
                # Collapsible thinking summary
                char_count = len(self.thinking)
                indicator = "▼" if self._show_thinking else "▶"
                parts.append(Text(f"{indicator} Thinking ({char_count} chars)", style="dim"))
                if self._show_thinking:
                    # Show thinking content indented
                    preview = self.thinking[:500]
                    if len(self.thinking) > 500:
                        preview += "..."
                    for line in preview.splitlines():
                        parts.append(Text(f"  │ {line}", style="dim italic"))

        # Main text
        if self.text:
            if self.done:
                parts.append(Markdown(self.text))
            else:
                if self._highlighter.has_code_blocks():
                    highlighted = self._highlighter.render_highlighted()
                    parts.extend(highlighted)
                    parts.append(Text("▍"))
                else:
                    parts.append(Text(self.text + "▍"))
        elif not self.done and not self.thinking:
            parts.append(Spinner("dots", text="Thinking...", style="dim italic"))

        # Toolcall preview (streaming only)
        if self.toolcalls and not self.done:
            preview = sorted(self.toolcalls.items())[-1][1]
            name = preview.name.strip()
            if name:
                key_arg = extract_key_arg_from_json(name, preview.args)
                tc = Text()
                tc.append("⏺ ", style="dim cyan")
                tc.append(normalize_tool_name(name), style="bold")
                if key_arg:
                    tc.append(f" {key_arg}", style="dim")
                parts.append(tc)

        if self.error:
            parts.append(Text(f"✗ Error: {self.error}", style="red"))

        result = Group(*parts) if parts else Text("")

        if self.done:
            self._cached_render = result

        return result
```

Note: toolcall preview `⏺` no longer has leading 2-space indent. Error prefix uses `✗`.

**Step 3: Run lint and tests**

```bash
uvx ruff check src/gen_agent/interactive/blocks.py
uv run pytest tests/unit/test_interactive_live_view.py -v
```

Expected: All pass.

**Step 4: Commit**

```bash
git add src/gen_agent/interactive/blocks.py
git commit -m "feat: collapsible thinking display in AssistantBlock"
```

---

### Task 4: Rework ToolRunBlock.render() — compact display, borderless diff

**Files:**
- Modify: `src/gen_agent/interactive/blocks.py:151-249`

**Step 1: Rewrite ToolRunBlock.render()**

Replace the `render()` method (lines 194-249) with:

```python
    def render(self) -> RenderableType:
        key_arg = self._key_arg()
        display_name = normalize_tool_name(self.name)

        if self.status == "running":
            label = Text()
            label.append(f"{display_name}", style="bold")
            if key_arg:
                label.append(f" {key_arg}", style="dim")
            return Spinner("dots", text=label)

        # Done state
        line = Text()
        if self.is_error:
            line.append("✗ ", style="red")
        else:
            line.append("✓ ", style="green")
        line.append(display_name, style="bold")
        if key_arg:
            line.append(f" {key_arg}", style="dim")

        # Change summary inline
        change_info = None
        if not self.is_error and self.result:
            change_info = extract_file_change_info(self.name, self.args, self.result)
            if change_info:
                _file_path, old_content, new_content = change_info
                diff_summary = summarize_diff(old_content, new_content)
                line.append(f" ({diff_summary})", style="cyan dim")

        if self.duration > 0.1:
            line.append(f" ({self.duration:.1f}s)", style="dim")

        if self.is_error and self.result_summary:
            line.append(f" — {self.result_summary}", style="dim")

        parts: list[RenderableType] = [line]

        # Expandable hint on next line
        if self.is_error and self.error_detail:
            hint_text = "Hide details" if self._show_details else "Show details"
            indicator = "▼" if self._show_details else "▶"
            parts.append(Text(f"  {indicator} {hint_text}", style="dim"))
        elif change_info is not None:
            hint_text = "Hide diff" if self._show_diff else "Show diff"
            indicator = "▼" if self._show_diff else "▶"
            parts.append(Text(f"  {indicator} {hint_text}", style="dim"))

        # Expanded error details (indented, no Panel)
        if self.is_error and self.error_detail and self._show_details:
            for err_line in self.error_detail.splitlines()[:20]:
                parts.append(Text(f"    {err_line}", style="red dim"))

        # Expanded diff (indented, no Panel)
        if not self.is_error and self._show_diff and change_info:
            _file_path, old_content, new_content = change_info
            diff_view = render_diff(old_content, new_content, _file_path)
            parts.append(Text("    ", style=""))  # spacer
            parts.append(diff_view)

        return Group(*parts) if len(parts) > 1 else line
```

Key changes:
- No leading 2-space on `✓`/`✗`
- Duration uses `.1f` (one decimal)
- Expand/collapse on separate line with descriptive text
- Error details rendered as indented lines (no Panel)
- Diff still uses `render_diff` but no Panel wrapping

**Step 2: Remove Panel import if unused**

Check if `Panel` is still used in blocks.py. If not, remove `from rich.panel import Panel` (line 8).

**Step 3: Run lint and tests**

```bash
uvx ruff check src/gen_agent/interactive/blocks.py
uv run pytest tests/unit/test_interactive_live_view.py -v
```

Expected: All pass. Test `test_live_view_tracks_tool_start_and_end` checks for "Read" and "README.md" — key_arg for path "README.md" stays unchanged (basename is same), so assertion still holds.

**Step 4: Commit**

```bash
git add src/gen_agent/interactive/blocks.py
git commit -m "feat: compact tool display with borderless diff"
```

---

### Task 5: Update notice rendering with icons

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py:290-300` (`add_notice`)
- Modify: `src/gen_agent/interactive/live_view.py:404-413` (`_commit_entries`)
- Modify: `src/gen_agent/interactive/live_view.py:434-438` (`_build_renderable` footer notices)

**Step 1: Add notice icon helper**

Add at module level in `live_view.py` (after the `_MAX_VISIBLE_NOTICES` line):

```python
_NOTICE_ICONS = {"info": "ℹ", "warning": "⚠", "error": "✗"}
_NOTICE_COLORS = {"info": "dim", "warning": "yellow", "error": "red"}
```

**Step 2: Update add_notice — use icon prefix**

In `add_notice()`, change the early-return console.print line (line 293) to use icon:

```python
    def add_notice(self, message: str, *, level: str = "info") -> None:
        icon = _NOTICE_ICONS.get(level, "ℹ")
        color = _NOTICE_COLORS.get(level, "dim")
        if self._live is None:
            self._console.print(Text(f"{icon} {message}", style=color))
            return
        ttl = _NOTICE_TTL_SECONDS.get(level, _NOTICE_TTL_SECONDS["info"])
        self._notices.append((level, message, time.monotonic() + ttl))
        self._notices = self._notices[-8:]
        if level == "error":
            self._sticky_error_notice = message
        self.request_refresh()
```

**Step 3: Update _commit_entries — use icon prefix**

In `_commit_entries()` (line 411-413), change the notice rendering:

```python
        for level, text in notices:
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            self._console.print(Text(f"{icon} {text}", style=color))
```

**Step 4: Update _build_renderable — use icon prefix in footer**

In `_build_renderable()` (line 435-438), change the notice rendering:

```python
        notices = self._active_notices()
        if notices:
            level, text = notices[-1]
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            footer_parts.append(Text(f"{icon} {text}", style=color))
```

**Step 5: Run tests**

```bash
uv run pytest tests/unit/test_interactive_live_view.py -v
```

Expected: `test_live_view_notice_ttl_expires` checks for "temporary" text — still passes since the icon is prepended but the text remains.

**Step 6: Commit**

```bash
git add src/gen_agent/interactive/live_view.py
git commit -m "feat: add icons to notice messages (ℹ/⚠/✗)"
```

---

### Task 6: Update status_items format and interrupt message

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py:440-442` (status_items in `_build_renderable`)
- Modify: `src/gen_agent/interactive/ptk_app.py:190` (interrupt message)

**Step 1: Change status_items format — values only, no key=**

In `_build_renderable()`, change line 441 from:

```python
            status_line = " · ".join(f"{key}={value}" for key, value in self._status_items.items())
```

to:

```python
            status_line = " · ".join(self._status_items.values())
```

**Step 2: Update interrupt message**

In `src/gen_agent/interactive/ptk_app.py`, change line 190 from:

```python
        self._live_view.add_notice("Interrupted (Ctrl+C again to quit)", level="warning")
```

to:

```python
        self._live_view.add_notice("Interrupted — Ctrl+C again to force quit", level="warning")
```

**Step 3: Update test assertion**

In `tests/unit/test_interactive_live_view.py`, the test `test_live_view_renders_title_header_footer_and_status` (line 225) currently asserts `"sync=ok"`. Change to:

```python
    assert "ok" in rendered
```

**Step 4: Run lint and tests**

```bash
uvx ruff check src/gen_agent/interactive/live_view.py src/gen_agent/interactive/ptk_app.py
uv run pytest tests/unit/test_interactive_live_view.py tests/unit/test_interactive_mode.py -v
```

Expected: All pass.

**Step 5: Commit**

```bash
git add src/gen_agent/interactive/live_view.py src/gen_agent/interactive/ptk_app.py tests/unit/test_interactive_live_view.py
git commit -m "refactor: status values only, clearer interrupt message"
```

---

### Task 7: Add toggle_thinking support in LiveView

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py:321-329` (`toggle_last_tool_details`)

**Step 1: Add toggle_last_thinking method**

Add after `toggle_last_tool_details()` in `live_view.py`:

```python
    def toggle_last_thinking(self) -> None:
        for entry in reversed(self._entries):
            if isinstance(entry, AssistantBlock) and entry.thinking:
                entry.toggle_thinking()
                self.request_refresh()
                break
```

**Step 2: Run tests**

```bash
uv run pytest tests/unit/test_interactive_live_view.py -v
```

Expected: All pass (no existing tests broken; new method is additive).

**Step 3: Commit**

```bash
git add src/gen_agent/interactive/live_view.py
git commit -m "feat: add toggle_last_thinking support"
```

---

### Task 8: Full validation

**Step 1: Run full lint**

```bash
uvx ruff check src/gen_agent/interactive/ src/gen_agent/extensions/ui.py src/gen_agent/modes/rpc_mode.py
```

Expected: All checks passed.

**Step 2: Run full test suite**

```bash
uv run pytest tests/unit tests/integration -q
```

Expected: All pass (integration test `test_rpc_extended_commands` may fail due to external API rate limits — that's pre-existing and unrelated).

**Step 3: Verify no broken imports**

```bash
uv run python -c "from gen_agent.interactive import GenInteractiveApp, RenderEngine, EventProcessor; print('OK')"
```

Expected: `OK`
