# gen-agent

Python reimplementation of the `pi` coding agent, built with `Typer` + `Pydantic v2`.

## Project Background & Goals

- Rebuild `pi-mono` core capabilities in Python for a unified engineering stack.
- Keep high compatibility for daily coding workflows: session tree, tool loop, resource loading, provider switching.
- Deliver a production-usable CLI (`gen`) with `interactive/print/json` as core paths.
- Keep scope explicit: no `/share`, `/export`, package-manager subcommands, OAuth login flow, or TypeScript extension bridge.

## Features

- CLI command: `gen`
- Modes: `interactive`, `print`, `json`, `rpc`
- Interactive UI: three-pane layout with live stream, inspector, picker, and keyboard-first navigation
- Non-zero exit codes for provider error/aborted responses in `print`/`json` modes
- Providers: OpenAI + Anthropic
- Usage cost accounting from optional per-model pricing in `models.json`
- Session tree with JSONL persistence and migration (`v1`/`v2`/`v3` -> current)
- Built-in tools: `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`
- Resource system: skills, prompt templates, themes, context files
- Python-native extension API

## Progress Summary

- Current status: core `pi` coding workflow is aligned for daily use (agent loop, sessions, tools, resources, OpenAI/Anthropic).
- Interactive mode is aligned on visual+behavior feature parity for core coding flow (three-pane UI, stream rendering, keyboard-first selectors, slash completion/history).
- Partially aligned: full RPC protocol parity.
- Intentionally out of scope: `/share`, `/export`, `/login`, `/logout`, package-manager commands, OAuth flow, TypeScript extension bridge.
- Full matrix: see `/Users/chen/workspace/gen/docs/compatibility.md`.

## Install / Run

```bash
uv run gen --help
```

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

## Notes

- Not implemented in this build: `/share`, `/export`, OAuth login flow, package-manager subcommands.
- Supported platforms: macOS, Linux.
