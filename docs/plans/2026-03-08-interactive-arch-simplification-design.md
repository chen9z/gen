# Interactive Architecture Simplification Design

Date: 2026-03-08
Status: Approved

## Goal

Simplify interactive module architecture: flatten property forwarding, merge duplicate reset logic, delete dead code, eliminate remaining duplication and encapsulation violations.

## Design

### 1. Flatten Property Forwarding + Slim RenderEngine

Move `_dirty`, `_last_activity_time`, `_flush_task`, `_min_interval`, `_max_interval` from RenderEngine to LiveView as direct attributes. RenderEngine becomes a minimal Rich Live manager:

```python
class RenderEngine:
    """Manages Rich Live instance lifecycle."""
    def __init__(self, console: Console): ...
    def start(self) -> None: ...
    def stop(self) -> None: ...       # only stops Live, does NOT cancel flush_task
    def flush(self, renderable) -> None: ...
    @property
    def is_active(self) -> bool: ...   # _live is not None
```

LiveView changes:
- Delete 6 property forwarding pairs (~40 lines)
- Own `_dirty`, `_last_activity_time`, `_flush_task`, `_min_interval`, `_max_interval` directly
- `request_refresh()` no longer calls RenderEngine.request_refresh() (delete that method)
- `stop()` cancels `_flush_task` then calls `_render_engine.stop()`
- Replace `self._live is not None` checks with `self._render_engine.is_active`

### 2. Merge start/_reset_turn_state

`start()` calls `_reset_turn_state(clear_usage=True)` instead of duplicating 14 field resets:

```python
def start(self) -> None:
    if self._flush_task is not None:
        return
    self._reset_turn_state(clear_usage=True)
    self._last_activity_time = time.monotonic()
    loop = ...
    self._flush_task = loop.create_task(self._flush_loop()) if loop else None
```

### 3. Delete Dead Code

- Delete `src/gen_agent/interactive/shortcuts_dialog.py` — no callers, stale keybinding info
- Delete `LiveView.add_user_prompt()` — pure forwarding wrapper for `print_user_prompt()`; update callers to use `print_user_prompt` directly

### 4. Eliminate Duplication and Encapsulation Violations

**Unify `_normalize_widget_placement`**: Add to `extensions/ui.py`:

```python
def normalize_widget_placement(value: str, *, camel: bool = False) -> str:
    lowered = value.strip().lower()
    if lowered in {"beloweditor", "below_editor"}:
        return "belowEditor" if camel else "below_editor"
    return "aboveEditor" if camel else "above_editor"
```

Delete local definitions in `ptk_app.py` and `rpc_mode.py`.

**Extract `clear_interrupt_state()`**: Replace `self._live_view._toolcall_phase.clear()` in ptk_app with:

```python
# LiveView
def clear_interrupt_state(self) -> None:
    self._toolcall_phase.clear()

# ptk_app
self._live_view.clear_interrupt_state()
```

## Files Affected

| Action | File |
|--------|------|
| Delete | `src/gen_agent/interactive/shortcuts_dialog.py` |
| Modify | `src/gen_agent/interactive/render_engine.py` — slim to Live manager |
| Modify | `src/gen_agent/interactive/live_view.py` — own state, merge start/reset, add clear_interrupt_state |
| Modify | `src/gen_agent/interactive/ptk_app.py` — use clear_interrupt_state, import normalize_widget_placement |
| Modify | `src/gen_agent/extensions/ui.py` — add normalize_widget_placement |
| Modify | `src/gen_agent/modes/rpc_mode.py` — import normalize_widget_placement |

## Validation

```bash
uvx ruff check src/gen_agent/interactive/ src/gen_agent/extensions/ui.py src/gen_agent/modes/rpc_mode.py
uv run pytest tests/unit tests/integration -q
```
