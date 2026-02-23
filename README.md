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
- Interactive UI: three-pane layout with live stream, inspector, picker, and keyboard-first navigation
- Non-zero exit codes for provider error/aborted responses in `print`/`json` modes
- Providers: OpenAI + Anthropic
- Usage cost accounting from optional per-model pricing in `models.json`
- Session tree with JSONL persistence and migration (`v1`/`v2`/`v3` -> current)
- Built-in tools: `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`
- Prompt file/image expansion via `@path` (text files inline, images as attachments)
- Resource system: skills, prompt templates, themes, context files
- Python-native extension API

## Progress Summary

- Current status: core `pi` coding workflow is aligned for daily use (agent loop, sessions, tools, resources, OpenAI/Anthropic).
- Interactive mode is aligned on visual+behavior feature parity for core coding flow (three-pane UI, stream rendering, keyboard-first selectors, slash completion/history).
- Partially aligned: full RPC protocol parity.
- Intentionally out of scope: `/changelog`, `/copy`, `/share`, `/export`, `/login`, `/logout`, package-manager commands, OAuth flow, TypeScript extension bridge.
- Full matrix: see `/Users/chen/workspace/gen/docs/compatibility.md`.

## Install / Run

```bash
uv run gen --help
```

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
/scoped-models openai/*
/tree
/tree 3
/fork
/resume
/compact
```

## Interactive shortcuts

```text
Ctrl+L/Ctrl+P  cycle model (forward)
Ctrl+Shift+P  cycle model (backward)
Ctrl+N  new session
Ctrl+R  open session picker
Ctrl+T  open tree picker
Ctrl+K  compact (/compact)
Tab/Shift+Tab  cycle pane focus (or apply slash suggestion when input has candidates)
Left/Right  switch active section in left pane (Sessions/Tree/Tools)
Up/Down/PageUp/PageDown  move picker selection, and navigate focused pane lists
Enter  confirm picker selection / confirm left-pane selection action
1-9  quick select current focused list item (picker and pane lists)
Esc  cancel picker; if no picker, clear slash suggestions or return focus to input
Ctrl+U  clear input
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
- Supported platforms: macOS, Linux.
