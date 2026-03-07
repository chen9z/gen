# Interactive UI Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix streaming visual jump, show all active notices, and clean up dead code in the interactive module.

**Architecture:** Three independent changes: (1) use Markdown during streaming to match done state, (2) render all notices instead of just the last one, (3) rename/delete dead code across the export chain.

**Tech Stack:** Python 3.11+, Rich (Markdown, Text, Spinner)

---

## Task 1: Fix streaming→done visual jump

**Files:**
- Modify: `src/gen_agent/interactive/blocks.py:129-139`

**Step 1: Update streaming text rendering in AssistantBlock.render()**

In `src/gen_agent/interactive/blocks.py`, find the `render()` method's main text section (around line 129). The current code is:

```python
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
```

Replace the `else` branch (non-code-block streaming) to use Markdown:

```python
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
                    parts.append(Markdown(self.text))
                    parts.append(Text("▍"))
```

Only change: line `parts.append(Text(self.text + "▍"))` → two lines: `parts.append(Markdown(self.text))` then `parts.append(Text("▍"))`.

**Step 2: Run tests**

Run: `uv run pytest tests/unit/test_interactive_live_view.py tests/unit/test_interactive_mode.py -v`
Expected: All pass

---

## Task 2: Show all active notices

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py:400-405`

**Step 1: Update notice rendering in `_build_renderable()`**

In `src/gen_agent/interactive/live_view.py`, find the notice rendering section in `_build_renderable()`. The current code is:

```python
        notices = self._active_notices()
        if notices:
            level, text = notices[-1]
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            footer_parts.append(Text(f"{icon} {text}", style=color))
```

Replace with:

```python
        for level, text in self._active_notices():
            icon = _NOTICE_ICONS.get(level, "ℹ")
            color = _NOTICE_COLORS.get(level, "dim")
            footer_parts.append(Text(f"{icon} {text}", style=color))
```

This renders all active notices (up to `_MAX_VISIBLE_NOTICES=2`) instead of only the last one.

**Step 2: Run tests**

Run: `uv run pytest tests/unit/test_interactive_live_view.py -v`
Expected: All pass

---

## Task 3: Rename `_mooning_spinner` → `_idle_spinner`

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py` (~5 references)
- Modify: `src/gen_agent/interactive/event_processor.py` (~10 references)

**Step 1: Rename in live_view.py**

Find-and-replace `_mooning_spinner` → `_idle_spinner` in `src/gen_agent/interactive/live_view.py`. Affected lines:

- `__init__`: `self._mooning_spinner: Spinner | None = None`
- `_reset_turn_state`: `self._mooning_spinner = None`
- `_has_live_content`: `self._mooning_spinner is not None`
- `_build_renderable`: `if self._mooning_spinner is not None`
- `_build_renderable`: `main_parts.append(self._mooning_spinner)`

**Step 2: Rename in event_processor.py**

Find-and-replace `_mooning_spinner` → `_idle_spinner` in `src/gen_agent/interactive/event_processor.py`. Affected locations:

- `_clear_mooning_spinner` method → rename to `_clear_idle_spinner`
- Inside `_clear_mooning_spinner`: `self._view._mooning_spinner` → `self._view._idle_spinner`
- `_on_agent_start`: `v._mooning_spinner = Spinner("dots", "")`
- `_on_agent_end`: `v._mooning_spinner = None`
- All calls to `self._clear_mooning_spinner()` → `self._clear_idle_spinner()`

**Step 3: Run lint and tests**

Run: `uvx ruff check src/gen_agent/interactive/live_view.py src/gen_agent/interactive/event_processor.py`
Expected: No errors

Run: `uv run pytest tests/unit/test_interactive_live_view.py -v`
Expected: All pass

---

## Task 4: Delete LIVE_CHAR_LIMIT export chain

**Files:**
- Modify: `src/gen_agent/interactive/blocks.py:15` — delete constant
- Modify: `src/gen_agent/interactive/__init__.py` — remove from import and `__all__`
- Modify: `src/gen_agent/interactive/ptk_app.py:16` — remove import
- Modify: `src/gen_agent/interactive/ptk_app.py:338` — remove from `__all__`
- Modify: `src/gen_agent/modes/interactive_mode.py:4,6` — remove import and `__all__` entry

**Step 1: Delete from blocks.py**

Remove line 15:
```python
LIVE_CHAR_LIMIT = 8000
```

**Step 2: Remove from `__init__.py`**

In `src/gen_agent/interactive/__init__.py`, change import line:
```python
from .ptk_app import GenInteractiveApp, LIVE_CHAR_LIMIT, PtkExtensionUIContext, run_interactive_mode
```
to:
```python
from .ptk_app import GenInteractiveApp, PtkExtensionUIContext, run_interactive_mode
```

Remove `"LIVE_CHAR_LIMIT"` from the `__all__` list.

**Step 3: Remove from ptk_app.py**

Delete import line 16:
```python
from .blocks import LIVE_CHAR_LIMIT
```

Remove `"LIVE_CHAR_LIMIT"` from `__all__` (line 338).

**Step 4: Remove from interactive_mode.py**

In `src/gen_agent/modes/interactive_mode.py`, change:
```python
from gen_agent.interactive.ptk_app import GenInteractiveApp, run_interactive_mode
from gen_agent.interactive.blocks import LIVE_CHAR_LIMIT as _LIVE_CHAR_LIMIT

__all__ = ["GenInteractiveApp", "_LIVE_CHAR_LIMIT", "run_interactive_mode"]
```
to:
```python
from gen_agent.interactive.ptk_app import GenInteractiveApp, run_interactive_mode

__all__ = ["GenInteractiveApp", "run_interactive_mode"]
```

**Step 5: Run lint and tests**

Run: `uvx ruff check src/gen_agent/interactive/ src/gen_agent/modes/interactive_mode.py`
Expected: No errors

Run: `uv run pytest tests/unit tests/integration -q`
Expected: All pass

---

## Task 5: Delete side_by_side diff dead code

**Files:**
- Modify: `src/gen_agent/interactive/diff_renderer.py`

**Step 1: Remove `side_by_side` parameter from `render_diff`**

In `src/gen_agent/interactive/diff_renderer.py`, change the function signature:
```python
def render_diff(old_content: str, new_content: str, file_path: str = "", side_by_side: bool = False) -> RenderableType:
```
to:
```python
def render_diff(old_content: str, new_content: str, file_path: str = "") -> RenderableType:
```

Delete lines 24-25:
```python
    if side_by_side:
        return _render_side_by_side_diff(old_content, new_content)
```

Remove the `side_by_side` parameter from the docstring.

**Step 2: Delete `_render_side_by_side_diff` function**

Delete the entire function (lines 60-76).

**Step 3: Remove unused imports**

Remove `Columns` and `Panel` from the imports:
```python
from rich.columns import Columns
from rich.panel import Panel
```

(Only `Group`, `RenderableType`, and `Text` remain needed.)

**Step 4: Run lint and tests**

Run: `uvx ruff check src/gen_agent/interactive/diff_renderer.py`
Expected: No errors

Run: `uv run pytest tests/unit tests/integration -q`
Expected: All pass
