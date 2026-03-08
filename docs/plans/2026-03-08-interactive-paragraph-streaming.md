# Interactive Paragraph Streaming Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 让 interactive assistant 输出按稳定段落提交到 scrollback，减少 live 区重排，保持终端滚动自然。

**Architecture:** 在 `AssistantBlock` 内部区分已提交片段和尾部草稿；`LiveView` flush 时优先提交完成片段，只让当前草稿保留在 live 区。工具块和 notice 维持现状，避免扩大 UI 改动面。

**Tech Stack:** Python 3.11, Rich, prompt_toolkit, pytest

---

### Task 1: 为段落提交写失败测试

**Files:**
- Modify: `tests/unit/test_interactive_live_view.py`
- Modify: `tests/integration/test_interactive_flow.py`

**Step 1: Write the failing test**

新增测试覆盖：

- 一条 assistant 消息包含两个段落时，第一段在消息未结束前已进入 console scrollback
- 未完成尾段仍留在 `LiveView` 的 active renderable 中
- message 完成后不会重复打印已经提交过的段落

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_interactive_live_view.py tests/integration/test_interactive_flow.py -q`

Expected: 新增测试失败，现有逻辑无法区分 committed/draft。

### Task 2: 实现 AssistantBlock 段落缓冲

**Files:**
- Modify: `src/gen_agent/interactive/blocks.py`
- Test: `tests/unit/test_interactive_live_view.py`

**Step 1: Write minimal implementation**

- 给 `AssistantBlock` 增加 committed segment 存储
- 提供 `drain_committed_renderables()` 或等价接口
- `append_text()` 在空行或代码块闭合时切分并提交稳定片段
- `render()` 只渲染 committed 之后的草稿内容

**Step 2: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_interactive_live_view.py -q`

Expected: 段落提交流测试通过。

### Task 3: 改造 LiveView flush 提交流

**Files:**
- Modify: `src/gen_agent/interactive/live_view.py`
- Modify: `src/gen_agent/interactive/blocks.py`
- Test: `tests/integration/test_interactive_flow.py`

**Step 1: Write minimal implementation**

- `LiveView._commit_ready_entries()` 先排空 assistant block 的已提交 segment
- assistant block 只在最终无剩余草稿时才视为 fully committed
- `stop()` 时只补打印未提交的尾部内容

**Step 2: Run test to verify it passes**

Run: `uv run pytest tests/integration/test_interactive_flow.py -q`

Expected: scrollback 中段落只打印一次，live 停止后无残留重复输出。

### Task 4: 更新文档与验证

**Files:**
- Modify: `docs/compatibility.md`

**Step 1: Update docs**

补充 interactive 渲染说明，明确“段落式提交”“滚动自然”“live 区只保留未完成草稿”的行为。

**Step 2: Run verification**

Run: `uv run pytest tests/unit/test_interactive_live_view.py tests/integration/test_interactive_flow.py -q`

Run: `uvx ruff check src/gen_agent/interactive/blocks.py src/gen_agent/interactive/live_view.py tests/unit/test_interactive_live_view.py tests/integration/test_interactive_flow.py`

Expected: 全部通过。
