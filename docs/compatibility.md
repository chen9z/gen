# 兼容性矩阵

## 项目背景

- 原项目 `pi-mono` 功能完整，但以 TypeScript 生态为主；本项目目标是在 Python 技术栈中提供高兼容替代实现。
- 团队期望统一使用 Python 工具链（`Typer` + `Pydantic v2`），降低二次开发和维护门槛。
- 现有工作流需要保留 `pi` 的核心交互语义：会话树、工具调用循环、资源加载、命令式控制与多 provider 支持。

## 项目目标

- 交付可运行的 `gen` CLI，并覆盖核心模式：`interactive`、`print`、`json`（`rpc` 保持可用但非优先）。
- 对齐高频编码场景：多轮对话、工具闭环、会话恢复/分叉、自动压缩后持续对话。
- 保持会话与配置层高兼容（含 legacy 迁移），确保从 `pi` 迁移成本可控。
- 提供 Python 原生扩展与资源体系，支持按项目动态装载和热重载。
- 明确范围裁剪：暂不实现 `/changelog`、`/copy`、`/share`、`/export`、包管理子命令、OAuth 登录流、TypeScript 扩展桥接。

## 进度快照（2026-02-24）

- 总体情况：`interactive/print/json` 主工作流、会话树、工具循环、OpenAI/Anthropic 双 provider 已实现核心对齐。
- 对齐程度：日常编码场景（含 interactive 视觉+行为核心能力）为高对齐；协议边角场景为中等对齐。
- 范围说明：本项目明确排除 `/changelog`、`/copy`、`/share`、`/export`、`/login`、`/logout`，以及 OAuth 登录流、包管理子命令。

## 已对齐（已交付）

- CLI/运行时基线：`gen` 基于 `Typer`，边界契约基于 `Pydantic v2`，支持 `interactive|print|json|rpc` 模式。
- 非交互行为：管道输入默认进入 print 模式；多消息参数顺序执行；`print/json` 在 provider 错误时返回非 0 退出码；`@图片` 可作为图片附件直传模型。
- Provider：OpenAI 与 Anthropic 运行于同一 agent loop，保留 assistant 的 tool-call 历史。
- 会话运行时：JSONL 树结构持久化；支持 v1/v2/v3 迁移；`resume/continue` 可恢复 provider/model/thinking；支持 fork/tree/compact。
- 压缩能力：默认开启自动 compaction；支持手动 compaction；`keepRecentTokens` 预算生效。
- 工具层：`read/write/edit/bash` + `grep/find/ls`，包含 limit、截断提示与结构化 `details`。
- tools schema 对齐：`find` 改为 `pattern` 必填、`ls` 收敛为 `path/limit`；其余工具参数命名与 `pi-mono` 保持一致（`oldText/newText`、`ignoreCase` 等）。
- system prompt 对齐：采用与 `pi-mono` 一致的结构化构建流程（工具说明、按工具能力动态 guidelines、文档引导、context/skills 追加顺序、时间与 cwd 尾部注入）。
- interactive UI：已切换到 `prompt_toolkit + Rich` 单主视图（Claude 风格），采用 Rich Live 稳态渲染，保留命令驱动交互与轻量选择器。
- interactive 输入区边界：改为常驻会话视图 + 固定 bottom toolbar；输入区附近仅保留一处 token usage，显示在输入框下一行并靠右对齐。
- interactive UI 第二轮收敛：工具状态改为彩色原点并附完成态摘要；消息窗口按终端高度动态裁剪；notice 改为短时 toast；输入态 `Ctrl+C` 不再写入噪声提示。
- interactive 渲染细节优化：支持同消息多 toolcall 预览并按 `contentIndex` 解析增量；超长完成态正文避免 Markdown 重排闪烁；输入区 usage 按显示宽度裁剪，避免与 prompt 重叠；`Ctrl+Y` 切换 usage 明细（默认仅 `input/output`，详细模式再显示 `cache/cost`）。
- interactive 行为对齐：`Ctrl+R/Ctrl+T` 选择器、`Ctrl+L/Ctrl+P` 模型轮换、`Ctrl+N` 新会话、`Ctrl+K` 压缩、`Tab` 补全、`Up/Down` 历史、`Esc` 取消；picker/confirm/input/editor 统一使用共享 PTK dialog 样式与按钮文案。
- interactive 输入增强：`Ctrl-J/Alt-Enter` 多行、slash fuzzy 补全、`@` 路径补全（忽略 `.git/node_modules/.venv/dist/build` 等目录）、历史持久化（`~/.config/gen-agent/user-history/<cwd_md5>.jsonl`）。
- interactive 流式可视化增强：assistant 文本/thinking/toolcall 增量渲染，tool execution 以 in-progress/done 块持续展示。
- interactive 稳态渲染增强：启用会话级常驻 Rich Live transcript，多轮消息、工具块与 notice 在同一视图连续保留，避免按轮次 start/stop 带来的断层。
- 资源体系：skills/prompt templates/themes/context 文件发现；冲突诊断；`/reload` 诊断输出；`/skill:name` 注入。
- 扩展体系：Python 原生扩展 API（`register_tool`、`register_command`、`register_flag`、`on(event, handler)`），支持异步命令处理器。
- 扩展 UI（本轮 1:1 对齐范围）：`select/confirm/input/editor`、`notify`、`setStatus`、`setWidget`、`setHeader`、`setFooter`、`setTitle`、`setEditorText/getEditorText`、`setEditorComponent` 已在 interactive/rpc 路径接入（`uiExtensionsEnabled` 控制）；interactive 下 `header/footer/title` 现已进入常驻会话视图。
- 扩展 UI 已收敛为纯文本语义：`setWidget/setHeader/setFooter` 仅接受 `str | list[str] | None`；`setEditorComponent` 仅接受文本编辑配置对象；不再支持组件工厂与 `dispose` 生命周期。
- 扩展迁移文档：`/Users/chen/workspace/gen/docs/extensions-migration.md`
- 模型控制：scoped models（精确/通配/模糊）、thinking 后缀、前后向模型轮换、`models.json` 能力钳制。
- 配置与鉴权优先级：`CLI > auth.json > ENV > models.json(provider.apiKey)`；支持 XDG + 项目级配置合并。
- Session 查询接口保持兼容并扩展可选参数：`list_sessions(limit, offset, include_current)`、`get_tree(limit, include_root)`。

## 部分对齐

- RPC 对齐：已支持内部驱动与会话/模型控制，但不以全量协议 1:1 对齐为当前目标。
- 模型目录与轮换策略：已切换为 `ModelRegistry` 驱动（内置模型 + provider override + custom models + modelOverrides 合并视图）。
- 成本核算：在 `models.json` 提供 pricing 时可计算成本；未包含外部账单对账层。
- Provider 调用语义：主路径切换为 `stream_complete` 真流式；`complete` 通过流式兼容适配保留。

## 未对齐 / 不在范围

- 按计划暂不对齐的 slash 命令：`/changelog`、`/copy`、`/share`、`/export`、`/login`、`/logout`。
- 包管理命令族（`install/remove/update/list`）未注册。
- OAuth 鉴权流程未实现（当前仅 API key）。
- TypeScript 扩展兼容桥未实现（当前仅 Python 扩展 API）。

## 已实现功能

- `gen --mode interactive|print|json|rpc`
- Provider 选择（`--provider`、`--model`）
- 从 `~/.config/gen-agent/models.json` 加载全局模型目录
- `models.json` provider 字段支持：`baseUrl/apiKey/api/headers/authHeader/models/modelOverrides`
- custom models 以 `provider+id` upsert；同 id 替换，异 id 追加
- provider override-only 可覆盖内置模型 `baseUrl/headers`
- 模型能力钳制（`reasoning: false` 时 thinking 强制为 `off`）
- 会话启动参数（`--continue`、`--resume`、`--session`、`--session-dir`、`--no-session`）
- `resume/continue` 从会话历史恢复 provider/model/thinking
- 管道输入默认采用非交互 print 行为（`echo ... | gen`）
- 非交互模式下多消息参数按顺序执行
- `@文件` 参数支持文本展开，`@图片` 参数支持图片附件（含无后缀 magic-bytes 识别）
- CLI `--models` 与 `/scoped-models` 模型范围控制
- scoped 模型匹配支持精确/通配/模糊，可附带 `:thinking`
- scoped pattern 的无效 thinking 后缀会告警并回退到默认值
- 启动时 scoped 选模（未指定 `--model` 时，`--models` 选中 in-scope 默认/首个模型）
- 模型轮换优先选择有可用鉴权的 provider/model
- 模型+thinking 简写（`--model provider/id:thinking`、`/model provider/id:thinking`）
- `/model` 与 `--model` 支持模糊查找（如 `haiku`）
- 运行时资源参数（`--extension/-e`、`--skill`、`--prompt-template`、`--theme` 与 `--no-*`）
- system prompt 控制（`--system-prompt`、`--append-system-prompt`）
- 模型列表（`--list-models`、`--list-models-search`）
- `--list-models` 显示 thinking 能力（`yes/no/unknown`）
- API key 解析（`--api-key`、环境变量、auth 文件）
- 鉴权优先级稳定并有测试：`CLI > auth.json > ENV > models.json(provider.apiKey)`
- CLI `--api-key` 仅作用于启动 provider（避免跨 provider 泄漏）
- JSONL 会话持久化与树结构 entry
- legacy 会话迁移兼容
- 内置工具调用循环
- 统一 assistant 事件映射（`start/text/thinking/toolcall/done/error`，通过 `message_update` 输出）
- OpenAI/Anthropic 适配层保留 assistant tool-call/tool-use 历史，支持多轮工具调用
- print 模式在 provider 错误/中止时返回非 0
- json 模式在 provider 错误/中止时返回非 0
- read 工具支持图片附件（`image/*`）与文本截断续读提示
- read 工具支持通过 magic bytes 检测图片 MIME（无后缀图片可识别）
- `grep/find/ls` 支持 limit 与截断提示，行为接近 pi 默认语义
- `grep/find/ls` 返回结构化 tool-result `details`（limit/truncation 元数据）
- interactive 模式基于 `prompt_toolkit + Rich` 单主视图运行（无需 Textual）
- interactive 模式支持网络级真流式渲染（provider chunk/token 到达即增量输出，Live 微批量刷新减少闪烁）
- interactive 多轮对话采用常驻 transcript，用户消息提交后进入同一会话流，不再依赖 prompt_toolkit 默认回显
- interactive 模式支持会话选择器（`Ctrl+R`）与树节点选择器（`Ctrl+T`）
- interactive 输入支持 slash 命令补全（`Tab`）与历史回溯（`Up/Down`）
- interactive 支持 `Esc` 取消 picker/dialog
- 自动 compaction（默认开启）
- compaction 锚点选择遵守 `keepRecentTokens` 预算（保留最近上下文）
- fork 会话时写入 branch summary
- 资源热重载（`/reload`）与 skill 命令分发
- `/reload` 返回资源/扩展诊断（冲突与装载错误）
- `/skill:name` 展开为 skill prompt 块并进入常规 agent loop
- 扩展注册 CLI flags（`register_flag`），支持布尔/字符串解析
- `uiExtensionsEnabled` 设置项（`/settings set uiExtensionsEnabled true project`）用于启用扩展 UI 上下文桥接
- context 文件（`AGENTS.md` / `CLAUDE.md`）注入 system prompt
- context 发现优先级对齐：全局优先，再祖先目录；同目录优先 `AGENTS.md` 再 `CLAUDE.md`
- skills/prompts/themes 资源冲突诊断
- RPC 控制：模型/thinking/队列模式、tree/session 管理、compact/reload
- RPC `abort` 可中止进行中的 `prompt/continue` 执行并产出 `aborted` stop reason
- RPC `reload` 返回 diagnostics；`fork_session.leafId` 非法时返回明确错误
- RPC 扩展 UI：支持输出 `extension_ui_request`，并接受 `extension_ui_response` 以完成阻塞式对话
- live 集成测试默认跳过，需显式使用 `pytest --live` 启用（避免日常单测被在线调用拖慢）

## 命令对齐

当前构建支持：

- `/settings`（`get` / `set`，默认写入 project scope）
- `/model`
- `/scoped-models`（set/clear + cycle 约束）
- `/name`
- `/session`
- `/fork`（从当前/目标分支创建新会话）
- `/tree`（列出 entries 并按 id 切换叶子）
- `/new`
- `/resume`（按 index/path 列表与恢复）
- `/compact`（手动压缩）
- `/reload`
- `/quit`

未注册/不支持：

- `/changelog`
- `/copy`
- `/share`
- `/export`
- `/login`
- `/logout`
- 包管理命令：`install/remove/update/list`

## 与 pi-mono 的已知差异

- 扩展运行时为 Python 原生实现，不执行 TypeScript 扩展。
- interactive 模式已迁移到 PTK+Rich 单视图，不再保留 Textual 三栏实现与兼容分支。
- 模型配置机制已对齐 `pi-mono` 的 `ModelRegistry` 语义；OAuth 登录流仍未纳入本轮范围。
- 成本核算依赖 `models.json` 中的模型 pricing 字段。
