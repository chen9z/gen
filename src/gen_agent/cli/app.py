from __future__ import annotations

import asyncio
import base64
import sys
from pathlib import Path
from typing import Any

import typer

from gen_agent import __version__
from gen_agent.core.model_store import get_model_definition
from gen_agent.models.content import ImageContent
from gen_agent.models.prompt import PromptInput
from gen_agent.modes import run_interactive_mode, run_json_mode, run_print_mode, run_rpc_mode
from gen_agent.runtime import SessionRuntime
from gen_agent.tools import create_all_tools

app = typer.Typer(add_completion=False, no_args_is_help=False, help="gen - AI coding assistant")


def _parse_tools(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [part.strip() for part in value.split(",") if part.strip()]


def _detect_image_mime(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext == ".png":
        return "image/png"
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".gif":
        return "image/gif"
    if ext == ".webp":
        return "image/webp"
    if ext == ".bmp":
        return "image/bmp"
    if ext in {".tif", ".tiff"}:
        return "image/tiff"

    try:
        head = path.read_bytes()[:32]
    except Exception:
        return None

    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if head.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if head.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if head.startswith(b"BM"):
        return "image/bmp"
    if len(head) >= 12 and head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    if head.startswith((b"II*\x00", b"MM\x00*")):
        return "image/tiff"
    return None


def _build_prompt_inputs_from_tokens(tokens: list[str] | None, cwd: str) -> list[PromptInput]:
    file_parts: list[str] = []
    images: list[ImageContent] = []
    messages: list[str] = []
    for token in tokens or []:
        if token.startswith("@") and len(token) > 1:
            raw_path = token[1:]
            path = Path(raw_path).expanduser()
            if not path.is_absolute():
                path = (Path(cwd) / path).resolve()
            if not path.exists() or not path.is_file():
                raise typer.BadParameter(f"File argument not found: {raw_path}")
            mime = _detect_image_mime(path)
            if mime:
                data = base64.b64encode(path.read_bytes()).decode("utf-8")
                images.append(ImageContent(data=data, mimeType=mime))
                continue
            content = path.read_text(encoding="utf-8")
            file_parts.append(f'<file path="{path}">\n{content}\n</file>')
            continue
        messages.append(token)

    text_prompts: list[str]
    if file_parts and messages:
        first = "\n\n".join([*file_parts, messages[0]])
        text_prompts = [first, *messages[1:]]
    elif file_parts:
        text_prompts = ["\n\n".join(file_parts)]
    else:
        text_prompts = [m for m in messages if m.strip()]

    prompts = [PromptInput(text=text) for text in text_prompts]
    if images:
        if prompts:
            prompts[0].images.extend(images)
        else:
            prompts = [PromptInput(text="", images=images)]
    return prompts


def _prompt_inputs_to_cli_payload(prompts: list[PromptInput]) -> str | list[str] | PromptInput | list[PromptInput] | None:
    if not prompts:
        return None
    has_images = any(prompt.images for prompt in prompts)
    if not has_images:
        texts = [prompt.text for prompt in prompts if prompt.text.strip()]
        if not texts:
            return None
        if len(texts) == 1:
            return texts[0]
        return texts
    if len(prompts) == 1:
        return prompts[0]
    return prompts


def _read_piped_stdin() -> str | None:
    if sys.stdin.isatty():
        return None
    data = sys.stdin.read()
    content = data.strip()
    return content or None


def _resolve_append_system_prompt(value: str | None, cwd: str) -> str | None:
    if not value:
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (Path(cwd) / path).resolve()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def _parse_extension_flag_values(extra_args: list[str], flag_specs: dict[str, Any]) -> dict[str, bool | str]:
    values: dict[str, bool | str] = {}
    i = 0
    while i < len(extra_args):
        token = extra_args[i]
        i += 1
        if not token.startswith("--"):
            continue

        name_value = token[2:]
        if not name_value:
            continue
        if "=" in name_value:
            name, raw_value = name_value.split("=", 1)
        else:
            name, raw_value = name_value, None

        spec = flag_specs.get(name)
        if spec is None:
            raise typer.BadParameter(f"Unknown option: --{name}")

        flag_type = getattr(spec, "flag_type", "boolean")
        if flag_type == "string":
            if raw_value is not None:
                values[name] = raw_value
                continue
            if i < len(extra_args) and not extra_args[i].startswith("--"):
                values[name] = extra_args[i]
                i += 1
                continue
            raise typer.BadParameter(f"Missing value for --{name}")

        if raw_value is None:
            values[name] = True
            continue
        lowered = raw_value.lower()
        if lowered in {"1", "true", "yes", "on"}:
            values[name] = True
        elif lowered in {"0", "false", "no", "off"}:
            values[name] = False
        else:
            raise typer.BadParameter(f"Invalid boolean value for --{name}: {raw_value}")
    return values


def _extract_prefixed_extension_flags(
    tokens: list[str] | None,
    flag_specs: dict[str, Any],
) -> tuple[list[str], dict[str, bool | str]]:
    if not tokens:
        return [], {}

    prompt_tokens: list[str] = []
    values: dict[str, bool | str] = {}
    i = 0
    parsing_options = True

    while i < len(tokens):
        token = tokens[i]
        i += 1

        if not parsing_options:
            prompt_tokens.append(token)
            continue

        if token == "--":
            parsing_options = False
            continue

        if not token.startswith("--"):
            parsing_options = False
            prompt_tokens.append(token)
            continue

        name_value = token[2:]
        if not name_value:
            continue
        if "=" in name_value:
            name, raw_value = name_value.split("=", 1)
        else:
            name, raw_value = name_value, None

        spec = flag_specs.get(name)
        if spec is None:
            raise typer.BadParameter(f"Unknown option: --{name}")

        flag_type = getattr(spec, "flag_type", "boolean")
        if flag_type == "string":
            if raw_value is not None:
                values[name] = raw_value
                continue
            if i < len(tokens) and not tokens[i].startswith("--"):
                values[name] = tokens[i]
                i += 1
                continue
            raise typer.BadParameter(f"Missing value for --{name}")

        if raw_value is None:
            values[name] = True
            continue
        lowered = raw_value.lower()
        if lowered in {"1", "true", "yes", "on"}:
            values[name] = True
        elif lowered in {"0", "false", "no", "off"}:
            values[name] = False
        else:
            raise typer.BadParameter(f"Invalid boolean value for --{name}: {raw_value}")

    return prompt_tokens, values


def _build_session(
    cwd: str,
    provider: str | None,
    model: str | None,
    api_key: str | None,
    base_url: str | None,
    thinking: str | None,
    tools: list[str] | None,
    no_session: bool,
    session: str | None,
    session_dir: str | None,
    extensions: list[str] | None,
    no_extensions: bool,
    skills: list[str] | None,
    no_skills: bool,
    prompt_templates: list[str] | None,
    no_prompt_templates: bool,
    themes: list[str] | None,
    no_themes: bool,
    system_prompt: str | None,
    append_system_prompt: str | None,
    extension_flag_values: dict[str, bool | str] | None = None,
) -> SessionRuntime:
    return SessionRuntime(
        cwd=cwd,
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        thinking_level=thinking,
        tools=tools,
        persist_session=not no_session,
        session_file=session,
        session_dir=session_dir,
        extensions=extensions,
        no_extensions=no_extensions,
        skills=skills,
        no_skills=no_skills,
        prompt_templates=prompt_templates,
        no_prompt_templates=no_prompt_templates,
        themes=themes,
        no_themes=no_themes,
        system_prompt=system_prompt,
        append_system_prompt=append_system_prompt,
        extension_flag_values=extension_flag_values,
    )


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def main(
    ctx: typer.Context,
    message: list[str] | None = typer.Argument(None, help="Prompt messages"),
    mode: str = typer.Option("interactive", "--mode", help="interactive|print|json|rpc"),
    provider: str | None = typer.Option(None, "--provider", help="Provider name"),
    model: str | None = typer.Option(None, "--model", help="Model id or provider/model"),
    api_key: str | None = typer.Option(None, "--api-key", help="API key"),
    base_url: str | None = typer.Option(None, "--base-url", help="Provider base URL"),
    system_prompt: str | None = typer.Option(None, "--system-prompt", help="Override system prompt"),
    append_system_prompt: str | None = typer.Option(None, "--append-system-prompt", help="Append text or file content to system prompt"),
    thinking: str | None = typer.Option(None, "--thinking", help="off|minimal|low|medium|high|xhigh"),
    tools: str | None = typer.Option(None, "--tools", help="Comma-separated tools"),
    no_tools: bool = typer.Option(False, "--no-tools", help="Disable all tools"),
    no_session: bool = typer.Option(False, "--no-session", help="Run without session persistence"),
    session: str | None = typer.Option(None, "--session", help="Explicit session file"),
    session_dir: str | None = typer.Option(None, "--session-dir", help="Session directory"),
    continue_session: bool = typer.Option(False, "--continue", "-c", help="Continue previous session"),
    resume_session: bool = typer.Option(False, "--resume", "-r", help="Resume latest session"),
    models: str | None = typer.Option(None, "--models", help="Comma-separated model patterns for cycling"),
    extensions: list[str] | None = typer.Option(None, "--extension", "-e", help="Extension file/dir (repeatable)"),
    no_extensions: bool = typer.Option(False, "--no-extensions", help="Disable configured extensions"),
    skills: list[str] | None = typer.Option(None, "--skill", help="Skill file/dir (repeatable)"),
    no_skills: bool = typer.Option(False, "--no-skills", help="Disable skill discovery and loading"),
    prompt_templates: list[str] | None = typer.Option(None, "--prompt-template", help="Prompt template file/dir (repeatable)"),
    no_prompt_templates: bool = typer.Option(False, "--no-prompt-templates", help="Disable prompt template discovery and loading"),
    themes: list[str] | None = typer.Option(None, "--theme", help="Theme file/dir (repeatable)"),
    no_themes: bool = typer.Option(False, "--no-themes", help="Disable theme discovery and loading"),
    print_mode: bool = typer.Option(False, "--print", "-p", help="Shortcut for --mode print"),
    list_models: bool = typer.Option(False, "--list-models", help="List available models"),
    list_models_search: str | None = typer.Option(None, "--list-models-search", help="Filter text for --list-models"),
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
    cwd: str = typer.Option(str(Path.cwd()), "--cwd", help="Working directory"),
) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit(code=0)

    if list_models and not list_models_search and message:
        candidate = message[0]
        if candidate and not candidate.startswith("@"):
            list_models_search = candidate
            message = message[1:]

    if list_models:
        preview_session = _build_session(
            cwd=cwd,
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
            thinking=thinking,
            tools=[] if no_tools else _parse_tools(tools),
            no_session=no_session,
            session=session,
            session_dir=session_dir,
            extensions=extensions,
            no_extensions=no_extensions,
            skills=skills,
            no_skills=no_skills,
            prompt_templates=prompt_templates,
            no_prompt_templates=no_prompt_templates,
            themes=themes,
            no_themes=no_themes,
            system_prompt=system_prompt,
            append_system_prompt=_resolve_append_system_prompt(append_system_prompt, cwd),
        )
        models_list = preview_session.list_available_models(search=list_models_search)
        typer.echo("Available models:")
        for item in models_list:
            provider, _, model_id = item.partition("/")
            definition = get_model_definition(provider, model_id)
            if definition is None or definition.reasoning is None:
                thinking = "unknown"
            else:
                thinking = "yes" if definition.reasoning else "no"
            typer.echo(f"- {item} (thinking: {thinking})")
        raise typer.Exit(code=0)

    if print_mode:
        mode = "print"
    if mode == "text":
        mode = "interactive"
    stdin_content = _read_piped_stdin() if mode != "rpc" else None
    if stdin_content and mode == "interactive":
        mode = "print"
    if stdin_content:
        message = [stdin_content, *(message or [])]

    tool_names = [] if no_tools else _parse_tools(tools)
    if tool_names:
        available = set(create_all_tools(cwd).keys())
        unknown = [name for name in tool_names if name not in available]
        if unknown:
            known = ", ".join(sorted(available))
            raise typer.BadParameter(f"Unknown tool(s): {', '.join(unknown)}. Available: {known}")

    session_obj = _build_session(
        cwd=cwd,
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        thinking=thinking,
        tools=tool_names,
        no_session=no_session,
        session=session,
        session_dir=session_dir,
        extensions=extensions,
        no_extensions=no_extensions,
        skills=skills,
        no_skills=no_skills,
        prompt_templates=prompt_templates,
        no_prompt_templates=no_prompt_templates,
        themes=themes,
        no_themes=no_themes,
        system_prompt=system_prompt,
        append_system_prompt=_resolve_append_system_prompt(append_system_prompt, cwd),
    )
    extension_flag_values = _parse_extension_flag_values(
        list(ctx.args),
        session_obj.extension_runner.get_flags(),
    )
    message, prefixed_extension_flags = _extract_prefixed_extension_flags(
        message,
        session_obj.extension_runner.get_flags(),
    )
    extension_flag_values.update(prefixed_extension_flags)
    if extension_flag_values:
        session_obj.extension_flags.update(extension_flag_values)
    if models:
        patterns = [part.strip() for part in models.split(",") if part.strip()]
        session_obj.set_scoped_models(patterns)
        if not model and not continue_session and not resume_session:
            session_obj.apply_scoped_startup_model()
    if continue_session or resume_session:
        sessions = session_obj.list_sessions(limit=50)
        current = session_obj.session_file
        target = next((s["path"] for s in sessions if s["path"] != current), None)
        if target:
            session_obj.resume_session(target)
        elif resume_session:
            raise typer.BadParameter("No previous sessions found to resume")

    prompt_inputs = _build_prompt_inputs_from_tokens(message, cwd)
    prompt = _prompt_inputs_to_cli_payload(prompt_inputs)

    if mode == "rpc":
        code = asyncio.run(run_rpc_mode(session_obj))
        raise typer.Exit(code=code)
    if mode == "json":
        if not prompt and not continue_session:
            raise typer.BadParameter("json mode requires a prompt")
        code = asyncio.run(run_json_mode(session_obj, prompt or None))
        raise typer.Exit(code=code)
    if mode == "print":
        if not prompt and not continue_session:
            raise typer.BadParameter("print mode requires a prompt")
        code = asyncio.run(run_print_mode(session_obj, prompt or None))
        raise typer.Exit(code=code)
    if mode == "interactive":
        code = asyncio.run(run_interactive_mode(session_obj, initial_message=prompt or None))
        raise typer.Exit(code=code)

    raise typer.BadParameter(f"Unsupported mode: {mode}")


def run() -> None:
    app()


if __name__ == "__main__":
    run()
