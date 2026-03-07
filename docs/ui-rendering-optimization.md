# UI 渲染优化 - 对齐 Claude Code 风格

## 变更概要

### 第一轮 (初始 plan)

#### P1: Toolcall 预览修复
- 只显示最后 1 个 toolcall（减少噪音）
- 解析 args JSON 提取 key arg（而非显示原始 JSON）
- 使用 `⏺` 前缀 + 2 空格缩进
- 工具名首字母大写

#### P2: Usage 显示时机
- 移除流式期间的实时 usage 估算更新
- 仅在 `done=True` 时渲染 usage_text

#### P3: 工具结果摘要
- 默认不显示 `result_summary`
- 仅在 `is_error` 时显示错误摘要

#### P4: Thinking 渲染
- 流式期间：使用 Spinner 替代纯文本
- 完成后：不显示任何 thinking 标记

#### P5: 用户提示符
- `> ` → `❯ `，颜色从 cyan 改为 magenta

#### P6: 视觉层次
- ToolRunBlock 所有行添加 2 空格前缀
- AssistantBlock toolcall 预览添加 2 空格缩进

#### P7: 工具名大小写
- `✓ bash` → `✓ Bash`

### 第二轮 (深度审查)

#### P0 (Bug): Usage 缓存失效
- `set_usage_text()` 方法在设置 usage 时清除 `_cached_render`
- 修复 `message_end` 设置 usage 后缓存不更新的问题

#### P1: renderers.py 同步
- 同步所有优化到 `renderers.py`（⏺ 前缀、缩进、capitalize、only-error summary 等）

#### P2: extract_file_change_info 去重
- ToolRunBlock.render() 中计算一次 change_info 并复用

#### P3: Footer 仅工作时显示
- `Ctrl+C to interrupt` 仅在 `_working=True` 时渲染

#### P4: Welcome banner 轻量化
- 移除 Panel 框，使用简洁文本 `✻ gen-agent`

#### P5: 状态栏精简
- 移除 session、pending、status 等调试信息
- 只保留 model + thinking(非 off 时) + turn

#### P6: Tool name 规范化
- 新增 `tool_key_args.py` 共享模块
- `normalize_tool_name()` 使用映射表处理 camelCase 等边界情况

#### P7: Prompt separator 轻量化
- `Rule` 分隔线改为空行

#### P8: result_summary 惰性计算
- 非 error 路径不调用 `_summarize_tool_result()`

#### P9: _TOOL_KEY_ARGS 去重
- 提取到 `tool_key_args.py` 共享模块

#### P10: Spinner 与 cursor 不共存
- Thinking spinner 仅在无 text 流式输出时显示

#### P11: Done 后隐藏 toolcall 预览
- 完成后不显示冗余的 toolcall 预览行

## 修改文件
- `src/gen_agent/interactive/tool_key_args.py` — 新增共享模块
- `src/gen_agent/interactive/blocks.py` — 渲染逻辑重构
- `src/gen_agent/interactive/event_processor.py` — usage/result_summary 优化
- `src/gen_agent/interactive/renderers.py` — 同步渲染优化
- `src/gen_agent/interactive/live_view.py` — banner/separator/footer
- `src/gen_agent/interactive/render_engine.py` — footer 条件
- `src/gen_agent/interactive/layout.py` — 状态栏精简
- `src/gen_agent/interactive/diff_renderer.py` — 移除未用 import
- `src/gen_agent/interactive/shortcuts_dialog.py` — 移除未用 import
- `tests/unit/test_interactive_live_view.py` — 测试更新
- `tests/integration/test_interactive_flow.py` — 测试更新

## 第三轮（回退到 kimi-cli shell 模型）

### 架构调整
- 放弃 PTK 全屏固定布局与固定底部输入框
- interactive 主循环回退为浮动 `PromptSession.prompt_async()`
- 当前轮动态内容由 `Rich Live(transient=True)` 承载
- 本轮结束后 assistant/tool 写入 scrollback；usage 保留在下一次 prompt 的下方一行

### 交互语义
- 未满屏时，输入框随 scrollback 一起下移
- 满屏后依赖终端自然滚动，输入框视觉上贴底
- 欢迎区 `Panel` 仅在 interactive 启动时打印一次
- `header/footer/title/widget/status` 只作用于当前轮 live 区，不再作为固定页面 chrome

### 实现影响
- 删除 fixed-layout 专用 transcript 窗口与 `Application(full_screen=True)` 主路径
- 移除输入区局部擦除/整屏擦除补丁逻辑
- usage 固定在输入框下方一行并靠右对齐，仅显示 `input/output/cache`
- 多轮历史以终端 scrollback 为准，不再维护常驻 transcript 面板
