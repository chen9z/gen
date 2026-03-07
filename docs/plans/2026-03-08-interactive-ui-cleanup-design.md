# Interactive UI Design Cleanup

Date: 2026-03-08
Status: Approved

## Goal

Fix streaming-to-done visual jump, display all active notices, and clean up dead code in the interactive module.

## Design

### 1. Fix Streaming→Done Visual Jump

Problem: Streaming uses `Text(self.text + "▍")`, done uses `Markdown(self.text)`. Style jumps on completion.

Solution in `AssistantBlock.render()`:
- When streaming without code blocks: use `Markdown(self.text)` + `Text("▍")` instead of plain `Text`
- When streaming with code blocks: keep `StreamingSyntaxHighlighter` path (Markdown handles unclosed fences poorly)
- When done: `Markdown(self.text)` (unchanged)

### 2. Show All Active Notices

Problem: `_build_renderable` only renders `notices[-1]`, ignoring `_MAX_VISIBLE_NOTICES=2`.

Solution: Render all entries from `_active_notices()`:

```python
for level, text in notices:
    icon = _NOTICE_ICONS.get(level, "ℹ")
    color = _NOTICE_COLORS.get(level, "dim")
    footer_parts.append(Text(f"{icon} {text}", style=color))
```

### 3. Dead Code Cleanup

- Rename `_mooning_spinner` → `_idle_spinner` across LiveView and EventProcessor (~15 references)
- Delete `LIVE_CHAR_LIMIT` constant and entire export chain (blocks.py → __init__.py → ptk_app.py → interactive_mode.py)
- Delete `_render_side_by_side_diff()` and `render_diff`'s `side_by_side` parameter
- Remove unused `Columns` and `Panel` imports from diff_renderer.py

## Files Affected

| Action | File |
|--------|------|
| Modify | `src/gen_agent/interactive/blocks.py` — streaming Markdown, delete LIVE_CHAR_LIMIT |
| Modify | `src/gen_agent/interactive/live_view.py` — rename _mooning_spinner, fix notice rendering |
| Modify | `src/gen_agent/interactive/event_processor.py` — rename _mooning_spinner |
| Modify | `src/gen_agent/interactive/diff_renderer.py` — delete side_by_side |
| Modify | `src/gen_agent/interactive/__init__.py` — remove LIVE_CHAR_LIMIT export |
| Modify | `src/gen_agent/interactive/ptk_app.py` — remove LIVE_CHAR_LIMIT import |
| Modify | `src/gen_agent/modes/interactive_mode.py` — remove LIVE_CHAR_LIMIT re-export |

## Validation

```bash
uvx ruff check src/gen_agent/interactive/ src/gen_agent/modes/interactive_mode.py
uv run pytest tests/unit tests/integration -q
```
