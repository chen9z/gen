# gen-agent

Python reimplementation of the `pi` coding agent, built with `Typer` + `Pydantic v2`.

## Project Background & Goals

- Rebuild `pi-mono` core capabilities in Python for a unified engineering stack.
- Keep high compatibility for daily coding workflows: session tree, tool loop, resource loading, provider switching.
- Deliver a production-usable CLI (`gen`) with `interactive/print/json` as core paths.
- Keep scope explicit: no `/changelog`, `/copy`, `/share`, `/export`, `/login`, `/logout`, package-manager subcommands, OAuth login flow, or TypeScript extension bridge.

## Features

- CLI command: `gen`
- Modes: `interactive`, `print`, `json`, `rpc`
- Interactive UI: `prompt_toolkit + Rich` 单主视图（Claude 风格）+ 命令驱动选择器
- Interactive 输入增强：`Ctrl-J/Alt-Enter` 多行、slash fuzzy 补全、`@` 路径补全、按 cwd 隔离的历史持久化
- Interactive 渲染优化：Rich Live 全屏稳态刷新（减少闪烁/重复堆叠），会话区仅渲染最近窗口
- Non-zero exit codes for provider error/aborted responses in `print`/`json` modes
- Providers: OpenAI + Anthropic
- Usage cost accounting from optional per-model pricing in `models.json`
- Session tree with JSONL persistence and migration (`v1`/`v2`/`v3` -> current)
- Built-in tools: `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`
- Prompt file/image expansion via `@path` (text files inline, images as attachments)
- Resource system: skills, prompt templates, themes, context files
- Python-native extension API
- Extension UI 纯文本 primitives（`select/confirm/input/editor`、`setWidget/setHeader/setFooter/setTitle`、`setEditorText/getEditorText`、`setEditorComponent`）
- Provider 级真流式（`stream_complete`）：网络 chunk/token 到达即渲染

## Progress Summary

- Current status: core `pi` coding workflow is aligned for daily use (agent loop, sessions, tools, resources, OpenAI/Anthropic).
- Interactive mode is aligned on core coding flow with PTK+Rich single-view UX, slash completion/history, and lightweight pickers.
- Interactive mode now uses Rich Live steady rendering: assistant 增量流式、tool in-progress/done 块、底栏持续状态提示。
- Partially aligned: full RPC protocol parity.
- Intentionally out of scope: `/changelog`, `/copy`, `/share`, `/export`, `/login`, `/logout`, package-manager commands, OAuth flow, TypeScript extension bridge.
- Full matrix: see `/Users/chen/workspace/gen/docs/compatibility.md`.

## Install / Run

```bash
uv run gen --help
```

## OpenAI 兼容接口快速启动

项目运行时不会自动读取仓库根目录的 `.env`，需要先由 shell 加载环境变量。

```bash
cp .env_example .env
$EDITOR .env
set -a && source .env && set +a
uv run gen \
  --provider "$GEN_PROVIDER" \
  --model "$GEN_MODEL" \
  --base-url "$GEN_BASE_URL"
```

说明：

- `OPENAI_API_KEY` 会被 `openai` provider 自动读取。
- `GEN_BASE_URL` 用于 OpenAI 兼容接口；如果你直连官方 OpenAI，也可以保留 `https://api.openai.com/v1`。
- 如果你想之后直接执行 `uv run gen`，把同样的 `baseUrl`/模型配置写入 `~/.config/gen-agent/models.json`。

## Testing

```bash
# Unit + integration (live tests are skipped by default)
uv run pytest

# Run live integration tests explicitly
uv run pytest --live tests/integration/test_live_core_flow.py
```

Live tests read provider settings from environment variables or `<repo>/.env` (`PROVIDER`, `MODEL`,
`BASE_URL`, `API_KEY`).

## Basic usage

```bash
# Interactive mode
gen

# Print mode
gen --mode print "List files in current directory"

# Piped stdin auto-runs in print mode
echo "Summarize README.md" | gen

# JSON event stream
gen --mode json "Read pyproject.toml"

# RPC mode
gen --mode rpc

# Continue most recent previous session
gen --continue

# Resume latest existing session (error if none)
gen --resume

# Scope model cycling set
gen --models "openai/*,anthropic/*"

# Scoped models can include thinking overrides
gen --models "openai/*:high,anthropic/*:low"

# Model + thinking shorthand
gen --model openai/gpt-4o:high "Solve this complex task"

# Load extra resources and extensions
gen --extension ./my_ext.py --skill ./skills --prompt-template ./prompts --theme ./themes

# Use extension-registered CLI flags
gen --extension ./my_ext.py --plan --persona strict "run plan"

# Include files in the initial prompt
gen --mode print @README.md "Summarize this file"

# Include image attachments in the initial prompt
gen --mode print @screenshot.png "What's in this image?"

# Override/append system prompt
gen --system-prompt "You are strict about tests." --append-system-prompt ./extra-system.txt

# List available models (optionally filtered)
gen --list-models --list-models-search haiku

# Restrict enabled tools (unknown names now fail fast)
gen --tools read,bash,edit,write "run checks"
```

## Common slash commands

```text
/settings get retry.maxRetries
/settings set retry.maxRetries 5 project
/settings set uiExtensionsEnabled true project
/scoped-models openai/*
/tree
/tree 3
/fork
/resume
/compact
```

## Interactive shortcuts

```text
Ctrl+L  cycle model (forward)
Ctrl+P  cycle model (backward)
Ctrl+N  new session
Ctrl+R  open session picker
Ctrl+T  open tree picker
Ctrl+K  compact (/compact)
Tab  fuzzy completion (/commands and @paths)
Ctrl+J  insert newline
Alt+Enter  insert newline
Enter  accept completion (when menu open) / submit input
Up/Down  input history
Esc  cancel picker/dialog
```

## Configuration paths

- Global: `~/.config/gen-agent/`
- Project overrides: `<repo>/.gen/`
- Optional model catalog: `~/.config/gen-agent/models.json`

## models.json（ModelRegistry 语义）

- provider 支持字段：`baseUrl`、`apiKey`、`api`、`headers`、`authHeader`、`models`、`modelOverrides`
- 合并规则：
  - 内置模型 + provider 覆盖（`baseUrl`/`headers`）+ custom models（`provider+id` upsert）+ `modelOverrides`
  - `modelOverrides` 只覆盖指定字段，未声明字段继承内置模型
- 配置值解析：
  - `apiKey`/`headers` 的值支持 `!command`（执行命令取 stdout，进程内缓存）
  - 非 `!` 值按“环境变量名优先，否则字面量”解析
- 凭证优先级（破坏性变更）：`CLI --api-key > auth.json > ENV > models.json(provider.apiKey)`

示例 1：仅覆盖内置 provider 的请求端点/头部

```json
{
  "providers": {
    "openai": {
      "baseUrl": "https://proxy.example.com/v1",
      "headers": {
        "x-tenant": "TEAM_ID"
      }
    }
  }
}
```

示例 2：在内置 provider 上追加/替换模型

```json
{
  "providers": {
    "openai": {
      "baseUrl": "https://proxy.example.com/v1",
      "apiKey": "OPENAI_PROXY_KEY",
      "api": "openai-completions",
      "models": [
        { "id": "gpt-4o-mini", "reasoning": false },
        { "id": "proxy-only", "name": "proxy-only", "reasoning": false }
      ]
    }
  }
}
```

示例 3：对内置模型做精细覆盖（`modelOverrides`）

```json
{
  "providers": {
    "openai": {
      "modelOverrides": {
        "gpt-4o-mini": {
          "name": "mini-override",
          "cost": { "input": 2.5 },
          "headers": { "x-model": "mini" },
          "contextWindow": 200000
        }
      }
    }
  }
}
```

## Notes

- Not implemented in this build: `/changelog`, `/copy`, `/share`, `/export`, `/login`, `/logout`, OAuth login flow, package-manager subcommands.
- RPC mode emits `extension_ui_request`; blocking extension dialogs require client `extension_ui_response`.
- Extension UI 已升级为纯文本协议（breaking）：组件工厂/生命周期语义已移除，迁移见 `/Users/chen/workspace/gen/docs/extensions-migration.md`。
- Supported platforms: macOS, Linux.
