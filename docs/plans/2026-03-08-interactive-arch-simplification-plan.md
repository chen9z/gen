# Interactive Architecture Simplification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Flatten property forwarding, merge duplicate reset logic, delete dead code, and eliminate duplication/encapsulation violations in the interactive module.

**Architecture:** Move rendering state from RenderEngine to LiveView, making RenderEngine a minimal Rich Live manager. Consolidate start/reset logic. Extract shared helpers to `extensions/ui.py`.

**Tech Stack:** Python 3.11+, Rich, prompt_toolkit

---

## Task 1: Slim RenderEngine to minimal Live manager

**Files:**
- Modify: `src/gen_agent/interactive/render_engine.py` (full rewrite, 56 lines → ~30 lines)

RenderEngine currently holds `_dirty`, `_last_activity_time`, `_flush_task`, `_min_interval`, `_max_interval` — state that belongs in LiveView. Slim it to only manage the Rich Live instance.

**Step 1: Rewrite render_engine.py**

Replace the entire file with:

```python
from __future__ import annotations

from rich.console import Console, RenderableType
from rich.live import Live


class RenderEngine:
    """Manages Rich Live instance lifecycle."""

    def __init__(self, console: Console):
        self._console = console
        self._live: Live | None = None

    @property
    def is_active(self) -> bool:
        return self._live is not None

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
        if self._live:
            self._live.stop()
            self._live = None

    def flush(self, renderable: RenderableType) -> None:
        if self._live is not None:
            self._live.update(renderable, refresh=True)
```

Removed: `_dirty`, `_last_activity_time`, `_flush_task`, `_min_interval`, `_max_interval`, `request_refresh()`, `console` property, `batch_interval` param. Stop no longer cancels `_flush_task` (LiveView will own that).

**Step 2: Run lint**

Run: `uvx ruff check src/gen_agent/interactive/render_engine.py`
Expected: No errors

---

## Task 2: Flatten property forwarding in LiveView

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py` (lines 67, 79-117, 211-216, 237-248, 266-269)

Move state from RenderEngine into LiveView, delete all 6 forwarding property pairs, and update internal references.

**Step 1: Update `__init__` — own state directly, change RenderEngine constructor**

In `__init__` (line 67), change:

```python
self._render_engine = RenderEngine(self._console, batch_interval)
```

to:

```python
self._render_engine = RenderEngine(self._console)
self._dirty = True
self._last_activity_time = 0.0
self._flush_task: asyncio.Task[None] | None = None
self._min_interval = 0.05
self._max_interval = 0.2
```

**Step 2: Delete all 6 forwarding property pairs (lines 79-117)**

Delete the entire block from `@property def _live` through `@property def _max_interval` — all 6 property pairs (~39 lines).

**Step 3: Replace `self._live` references with `self._render_engine.is_active`**

In `request_refresh()` (line 215), change:

```python
if force and self._live is not None:
```

to:

```python
if force and self._render_engine.is_active:
```

In `_flush_once()` (line 242), change:

```python
if not self._dirty or self._live is None:
```

to:

```python
if not self._dirty or not self._render_engine.is_active:
```

In `_flush_render()` (line 247), change:

```python
if self._live is None:
```

to:

```python
if not self._render_engine.is_active:
```

In `_ensure_live_started()` (line 267), change:

```python
if self._live is not None or not self._has_live_content():
```

to:

```python
if self._render_engine.is_active or not self._has_live_content():
```

In `add_notice()` (line 295), change:

```python
if self._live is None:
```

to:

```python
if not self._render_engine.is_active:
```

**Step 4: Delete `request_refresh` delegation to RenderEngine**

In `request_refresh()` (line 214), remove:

```python
self._render_engine.request_refresh()
```

(LiveView now owns `_dirty` and `_last_activity_time` directly, the two assignments above are sufficient.)

**Step 5: Update `stop()` — cancel flush_task before RenderEngine.stop()**

In `stop()` (line 181-187), change:

```python
def stop(self) -> None:
    self._commit_ready_entries()
    entries = list(self._entries[self._committed_count:])
    notices = self._active_notices()
    self._render_engine.stop()
    self._commit_entries(entries, notices)
    self._reset_turn_state(clear_usage=False)
```

to:

```python
def stop(self) -> None:
    self._commit_ready_entries()
    entries = list(self._entries[self._committed_count:])
    notices = self._active_notices()
    if self._flush_task:
        self._flush_task.cancel()
        self._flush_task = None
    self._render_engine.stop()
    self._commit_entries(entries, notices)
    self._reset_turn_state(clear_usage=False)
```

**Step 6: Remove unused imports**

Remove `import time` if no longer needed at module level — but `time.monotonic()` is still used in multiple places, so keep it.

**Step 7: Run lint and tests**

Run: `uvx ruff check src/gen_agent/interactive/render_engine.py src/gen_agent/interactive/live_view.py`
Expected: No errors

Run: `uv run pytest tests/unit/test_interactive_live_view.py tests/unit/test_interactive_mode.py -v`
Expected: All pass

---

## Task 3: Merge start/_reset_turn_state

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py` (lines 156-179)

`start()` duplicates 14 field resets that `_reset_turn_state()` already does. Merge them.

**Step 1: Replace start() body**

Change `start()` (lines 156-179) from:

```python
def start(self) -> None:
    if self._flush_task is not None:
        return
    self._entries.clear()
    self._tool_runs.clear()
    self._draft = None
    self._active_toolcall_index = None
    self._toolcall_phase.clear()
    self._mooning_spinner = None
    self._working = False
    self._notices.clear()
    self._sticky_error_notice = None
    self._input_usage_parts = []
    self._reset_usage()
    self._current_turn = 0
    self._max_turns = 0
    self._committed_count = 0
    self._last_activity_time = time.monotonic()
    self._stream_tick = 0
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    self._flush_task = loop.create_task(self._flush_loop()) if loop is not None else None
```

to:

```python
def start(self) -> None:
    if self._flush_task is not None:
        return
    self._reset_turn_state(clear_usage=True)
    self._last_activity_time = time.monotonic()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    self._flush_task = loop.create_task(self._flush_loop()) if loop is not None else None
```

Note: `_reset_turn_state` already clears `_input_usage_parts` when `clear_usage=True`, resets `_stream_tick`, `_dirty`, and all other fields. The only things `start()` adds are setting `_last_activity_time` and creating the flush task.

**Step 2: Run tests**

Run: `uv run pytest tests/unit/test_interactive_live_view.py tests/unit/test_interactive_mode.py -v`
Expected: All pass

---

## Task 4: Delete dead code

**Files:**
- Delete: `src/gen_agent/interactive/shortcuts_dialog.py`
- Modify: `src/gen_agent/interactive/live_view.py` (line 355-356)

**Step 1: Delete shortcuts_dialog.py**

```bash
rm src/gen_agent/interactive/shortcuts_dialog.py
```

No callers exist (confirmed via grep).

**Step 2: Delete `add_user_prompt()` from LiveView**

Remove from `live_view.py` (lines 355-356):

```python
def add_user_prompt(self, message: str) -> None:
    self.print_user_prompt(message)
```

No external callers (confirmed via grep). `print_user_prompt()` is the canonical method.

**Step 3: Run lint and tests**

Run: `uvx ruff check src/gen_agent/interactive/`
Expected: No errors

Run: `uv run pytest tests/unit tests/integration -q`
Expected: All pass

---

## Task 5: Unify `_normalize_widget_placement`

**Files:**
- Modify: `src/gen_agent/extensions/ui.py` — add `normalize_widget_placement()`
- Modify: `src/gen_agent/interactive/ptk_app.py` — delete local `_normalize_widget_placement`, import shared version
- Modify: `src/gen_agent/modes/rpc_mode.py` — delete local `_normalize_widget_placement`, import shared version

**Step 1: Add `normalize_widget_placement` to extensions/ui.py**

After `normalize_lines()` (line 23), add:

```python
def normalize_widget_placement(value: str, *, camel: bool = False) -> str:
    """Normalize widget placement string to canonical form."""
    lowered = value.strip().lower()
    if lowered in {"beloweditor", "below_editor"}:
        return "belowEditor" if camel else "below_editor"
    return "aboveEditor" if camel else "above_editor"
```

**Step 2: Update ptk_app.py**

In imports (line 11), change:

```python
from gen_agent.extensions.ui import CamelCaseUIMixin, normalize_lines as _normalize_lines
```

to:

```python
from gen_agent.extensions.ui import CamelCaseUIMixin, normalize_lines as _normalize_lines, normalize_widget_placement
```

Delete the local `_normalize_widget_placement` function (lines 40-44).

In `PtkExtensionUIContext.set_widget()` (line 83), change:

```python
placement_token = _normalize_widget_placement(str(placement))
```

to:

```python
placement_token = normalize_widget_placement(str(placement))
```

**Step 3: Update rpc_mode.py**

In imports (line 12), change:

```python
from gen_agent.extensions.ui import CamelCaseUIMixin, normalize_lines as _normalize_lines
```

to:

```python
from gen_agent.extensions.ui import CamelCaseUIMixin, normalize_lines as _normalize_lines, normalize_widget_placement
```

Delete the local `_normalize_widget_placement` function (lines 19-23).

In `_resolve_widget_placement()` (lines 26-31), change both calls from `_normalize_widget_placement(...)` to `normalize_widget_placement(..., camel=True)`.

**Step 4: Run lint and tests**

Run: `uvx ruff check src/gen_agent/extensions/ui.py src/gen_agent/interactive/ptk_app.py src/gen_agent/modes/rpc_mode.py`
Expected: No errors

Run: `uv run pytest tests/unit tests/integration -q`
Expected: All pass

---

## Task 6: Extract `clear_interrupt_state()`

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py` — add `clear_interrupt_state()`
- Modify: `src/gen_agent/interactive/ptk_app.py` (line 189)

**Step 1: Add `clear_interrupt_state()` to LiveView**

After `clear_input_usage_text()` (around line 372), add:

```python
def clear_interrupt_state(self) -> None:
    """Clear tool-call phase tracking on interrupt."""
    self._toolcall_phase.clear()
```

**Step 2: Fix encapsulation violation in ptk_app.py**

In `_cancel_active_run()` (line 189), change:

```python
self._live_view._toolcall_phase.clear()
```

to:

```python
self._live_view.clear_interrupt_state()
```

**Step 3: Run full validation**

Run: `uvx ruff check src/gen_agent/interactive/ src/gen_agent/extensions/ui.py src/gen_agent/modes/rpc_mode.py`
Expected: No errors

Run: `uv run pytest tests/unit tests/integration -q`
Expected: All pass

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor: simplify interactive architecture

- Slim RenderEngine to minimal Rich Live manager
- Flatten property forwarding from LiveView to RenderEngine
- Merge start/_reset_turn_state duplicate logic
- Delete dead code (shortcuts_dialog.py, add_user_prompt)
- Unify _normalize_widget_placement in extensions/ui.py
- Extract clear_interrupt_state() to fix encapsulation violation"
```
