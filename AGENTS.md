# Repository Guidelines

## Project Structure & Module Organization
Core code is in `src/gen_agent/`:
- `cli/` for Typer entrypoints (`gen` command wiring).
- `core/` for session lifecycle, settings/auth/model stores, and agent loop logic.
- `modes/` for `interactive`, `print`, `json`, and `rpc` runtime paths.
- `providers/`, `tools/`, `resources/`, `extensions/`, and `models/` for integrations and shared schemas.

Tests are organized by scope:
- `tests/unit/` for focused component behavior.
- `tests/integration/` for end-to-end CLI/session flows.
- `tests/golden/` for snapshot-style fixtures (for example `json_event_stream.golden`).

Reference notes and parity tracking are in `docs/compatibility.md`.

## Build, Test, and Development Commands
- `uv sync --extra test` installs runtime and test dependencies.
- `uv run gen --help` verifies the CLI entrypoint.
- `uv run pytest` runs the full suite (`pyproject.toml` already sets `-q`).
- `uv run pytest tests/unit` runs only unit tests.
- `uv run pytest tests/integration` runs integration coverage.
- `uv build` creates source/wheel distributions via Hatchling.
- `uvx ruff check .` runs lint checks using the configured Ruff rules.

## Coding Style & Naming Conventions
- Target Python `3.11+`, 4-space indentation, and explicit type hints on new public APIs.
- Follow Ruff settings in `pyproject.toml` (line length `100`, target `py311`).
- Use `snake_case` for modules/functions, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Keep modules focused by domain (for example new provider logic belongs in `src/gen_agent/providers/`).

## Guidelines
- Output with CHINESE.
- update relevant docs ( `docs/`, this guide), and ensure storage artifacts stay untracked.
- Prefer minimal, concise code.
- Avoid excessive defensive programming unless handling user input or external data.

## Testing Guidelines
- Use `pytest` with `pytest-asyncio` for async behavior.
- Name files `test_*.py` and test functions `test_*`.
- Mark coroutine tests with `@pytest.mark.asyncio`.
- For behavior changes, add unit tests first and integration tests when CLI/session flow changes.

## Commit & Pull Request Guidelines
- Follow the observed commit pattern: `type: concise summary` (example: `chore: clean project content`).
- Prefer small, single-purpose commits.
- PRs should include a short problem/solution summary.
- PRs should include linked issue or context.
- PRs should include test evidence (commands run, such as `uv run pytest tests/unit`).
- PRs that change interactive behavior should include screenshots or terminal captures.

## Security & Configuration Tips
- Never commit credentials; use `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` via environment or local auth config.
- Global config lives under `~/.config/gen-agent/`; project overrides belong in `<repo>/.gen/`.

