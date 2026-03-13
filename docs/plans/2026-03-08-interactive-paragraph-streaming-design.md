# Interactive Paragraph Streaming Design

**Date:** 2026-03-08

**Goal:** 让 interactive 模式在流式输出时按稳定段落提交，减少整块 Markdown 重排，保证终端滚动自然，避免 live 区上下跳动。

## 背景

当前 interactive 渲染把 assistant 草稿作为一个整体反复 `Markdown(...)` 重绘。对于长段落、列表、未闭合代码块，这会导致：

- 同一批已输出内容在 live 区被重复重排
- 已经“稳定”的文本仍跟随草稿一起抖动
- 输出进入 scrollback 的时机过晚，终端滚动不像自然追加

这和目标交互不一致。当前优先级不是更强的流式 Markdown，而是稳定渲染。

## 方案

采用“段落式提交”：

- assistant 输出拆成两部分：
  - `committed_segments`：已经稳定、可直接打印到 scrollback 的片段
  - `draft_text`：当前未完成的尾部草稿，只在 live 区显示
- 只在遇到稳定边界时提交片段：
  - 空行分隔的段落结束
  - fenced code block 闭合
  - message `done/error`
- `LiveView` 在 flush 时优先把已经完成的 committed segment 打进 scrollback
- live 区只保留当前未完成草稿、正在执行的 tool、notice 和状态行

## 边界与取舍

- 流式阶段的 Markdown 效果会弱于整块重绘，属于有意取舍
- 不做 AST 级增量 Markdown 更新，避免复杂度和闪烁风险
- 本轮不扩展新的 UI 布局，只修正数据提交流和滚动语义

## 预期行为

- 长文本输出时，已经结束的段落会自然滚入 scrollback
- 未结束的最后一段仍在 live 区增量更新
- 代码块在闭合前保持草稿显示，闭合后整体提交
- 消息完成时，不会再重复打印已提交内容

## 影响文件

- `src/gen_agent/interactive/blocks.py`
- `src/gen_agent/interactive/live_view.py`
- `tests/unit/test_interactive_live_view.py`
- `tests/integration/test_interactive_flow.py`
- `docs/compatibility.md`
