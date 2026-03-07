from __future__ import annotations

import json
import re
import shlex
from collections.abc import AsyncIterator
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from gen_agent.core.auth_store import AuthStore
from gen_agent.core.compaction import (
    build_compaction_message,
    estimate_message_tokens,
    generate_compaction_summary,
    should_compact,
)
from gen_agent.core.model_registry import ModelRegistry
from gen_agent.core.session_manager import SessionManager
from gen_agent.core.settings_store import load_settings, save_settings
from gen_agent.core.system_prompt import build_system_prompt
from gen_agent.extensions import ExtensionUIContext, ExtensionRunner, NoOpExtensionUIContext
from gen_agent.models.content import ImageContent, TextContent, UserContentBlock
from gen_agent.models.events import (
    AgentEnd,
    AgentEvent,
    AgentSessionEvent,
    AssistantMessageEvent,
    AutoCompactionEnd,
    AutoCompactionStart,
    MessageEnd,
    MessageStart,
    MessageUpdate,
    TurnEnd,
)
from gen_agent.models.messages import AgentMessage, AssistantMessage, UserMessage
from gen_agent.providers import ProviderRegistry, ProviderRequest
from gen_agent.providers.stream_types import ProviderStreamEvent, stream_events_from_assistant
from gen_agent.resources import ResourceLoader
from gen_agent.resources.frontmatter import parse_frontmatter
from gen_agent.tools import DEFAULT_TOOL_NAMES, ToolRegistry, create_all_tools

from .command_router import CommandRouter
from .event_emitter import EventEmitter
from .run_executor import RunExecutor


class SessionRuntime:
    def __init__(
        self,
        cwd: str,
        provider: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        thinking_level: str | None = None,
        tools: list[str] | None = None,
        persist_session: bool = True,
        session_file: str | None = None,
        session_dir: str | None = None,
        extensions: list[str] | None = None,
        no_extensions: bool = False,
        skills: list[str] | None = None,
        no_skills: bool = False,
        prompt_templates: list[str] | None = None,
        no_prompt_templates: bool = False,
        themes: list[str] | None = None,
        no_themes: bool = False,
        system_prompt: str | None = None,
        append_system_prompt: str | None = None,
        extension_flag_values: dict[str, bool | str] | None = None,
    ):
        self.cwd = str(Path(cwd).resolve())
        self.global_settings, self.project_settings, self.settings = load_settings(self.cwd)

        self.provider_registry = ProviderRegistry()
        self.auth = AuthStore()
        self.model_registry = ModelRegistry(auth_store=self.auth)
        self.resource_loader = ResourceLoader(self.cwd)
        self.extension_runner = ExtensionRunner()
        self.ui: ExtensionUIContext = NoOpExtensionUIContext()

        self._include_discovered_skills = not no_skills
        self._include_discovered_prompts = not no_prompt_templates
        self._include_discovered_themes = not no_themes
        self._skill_commands_enabled = self.settings.enable_skill_commands and not no_skills

        self._extra_skill_paths = [] if no_skills else [*self.settings.skills, *(skills or [])]
        self._extra_prompt_paths = [] if no_prompt_templates else [*self.settings.prompts, *(prompt_templates or [])]
        self._extra_theme_paths = [] if no_themes else [*self.settings.themes, *(themes or [])]
        self._extension_paths = [] if no_extensions else list(self.settings.extensions)
        self._extension_paths.extend(extensions or [])
        self.extension_flags: dict[str, bool | str] = dict(extension_flag_values or {})
        self._system_prompt_override = system_prompt
        self._append_system_prompt = append_system_prompt
        self._last_model_scope_warnings: list[str] = []

        self.resource_loader.reload(
            extra_skill_paths=self._extra_skill_paths,
            extra_prompt_paths=self._extra_prompt_paths,
            extra_theme_paths=self._extra_theme_paths,
            include_discovered_skills=self._include_discovered_skills,
            include_discovered_prompts=self._include_discovered_prompts,
            include_discovered_themes=self._include_discovered_themes,
        )
        self.extension_runner.load(self._extension_paths)
        self._scoped_model_patterns: list[str] = list(self.settings.enabled_models)

        self.session_manager = SessionManager(
            cwd=self.cwd,
            persist=persist_session,
            session_file=session_file,
            session_dir=session_dir,
        )

        parsed_model, model_thinking = self._split_model_thinking(model)
        provider_from_model, model_id = self._resolve_provider_and_model(provider, parsed_model)
        self.provider_name = provider_from_model
        self.model_id = model_id
        self.cli_api_key = api_key
        self.cli_api_key_provider = provider_from_model if api_key else None
        self.cli_base_url = base_url
        self.cli_base_url_provider = provider_from_model if base_url else None
        self.thinking_level = thinking_level or model_thinking or self.settings.default_thinking_level or "off"
        self._clamp_thinking_for_current_model()
        self.steering_mode = self.settings.steering_mode
        self.follow_up_mode = self.settings.follow_up_mode

        all_tools = create_all_tools(self.cwd, shell_command_prefix=self.settings.shell_command_prefix)
        enabled_names = tools or DEFAULT_TOOL_NAMES
        self._core_tools = [all_tools[name] for name in enabled_names if name in all_tools]
        self._rebuild_tool_registry()

        self._steering_queue: list[AgentMessage] = []
        self._follow_up_queue: list[AgentMessage] = []
        self.event_emitter = EventEmitter(self)
        self.command_router = CommandRouter(self)
        self.run_executor = RunExecutor(self)
        self._sync_runtime_from_session_context()

    @property
    def ui_extensions_enabled(self) -> bool:
        return bool(self.settings.ui_extensions_enabled)

    @property
    def available_tools(self) -> list[str]:
        return sorted(self.tool_registry.tools.keys())

    @property
    def session_file(self) -> str | None:
        return str(self.session_manager.file) if self.session_manager.file else None

    def bind_ui_context(self, context: ExtensionUIContext | None) -> None:
        if not self.ui_extensions_enabled or context is None:
            self.ui = NoOpExtensionUIContext()
            return
        self.ui = context

    def subscribe(self, listener):
        return self.event_emitter.subscribe(listener)

    def _emit(self, event: AgentSessionEvent | AgentEvent) -> AgentSessionEvent:
        return self.event_emitter.emit(event)

    def _rebuild_tool_registry(self) -> None:
        extension_tools = list(self.extension_runner.get_tools().values())
        self.tool_registry = ToolRegistry(self._core_tools + extension_tools)

    def _available_model_catalog(self) -> dict[str, list[str]]:
        self.model_registry.refresh()
        return self.model_registry.load_catalog()

    def _resolve_model_pattern(self, pattern: str, all_models: list[tuple[str, str]]) -> list[tuple[str, str]]:
        normalized = pattern.strip()
        if not normalized:
            return []

        lower_pattern = normalized.lower()
        model_tokens = [(provider, model, f"{provider}/{model}".lower()) for provider, model in all_models]

        if any(ch in normalized for ch in "*?["):
            matched: list[tuple[str, str]] = []
            for provider, model, token in model_tokens:
                if fnmatch(token, lower_pattern) or fnmatch(model.lower(), lower_pattern):
                    matched.append((provider, model))
            return matched

        for provider, model, token in model_tokens:
            if token == lower_pattern:
                return [(provider, model)]

        for provider, model, _token in model_tokens:
            if model.lower() == lower_pattern:
                return [(provider, model)]

        partial = [
            (provider, model)
            for provider, model, token in model_tokens
            if lower_pattern in token or lower_pattern in model.lower()
        ]
        if not partial:
            return []

        alias = [entry for entry in partial if self._is_model_alias(entry[1])]
        candidates = alias or partial
        candidates.sort(key=lambda item: item[1].lower(), reverse=True)
        return [candidates[0]]

    def _resolve_scoped_models_with_warnings(self) -> tuple[list[tuple[str, str, str | None]], list[str]]:
        catalog = self._available_model_catalog()
        all_models = [(provider, model) for provider, models in catalog.items() for model in models]
        if not self._scoped_model_patterns:
            return ([(provider, model, None) for provider, model in all_models], [])

        warnings: list[str] = []
        default_thinking = self.settings.default_thinking_level or "off"
        matched: list[tuple[str, str, str | None]] = []
        seen: set[tuple[str, str]] = set()
        for raw_pattern in self._scoped_model_patterns:
            pattern, thinking = self._split_model_thinking(raw_pattern)
            if not pattern:
                continue
            resolved = self._resolve_model_pattern(pattern, all_models)
            if not resolved and thinking is None and ":" in raw_pattern:
                base_pattern, invalid_level = raw_pattern.rsplit(":", 1)
                fallback = self._resolve_model_pattern(base_pattern, all_models) if base_pattern else []
                if fallback:
                    warnings.append(
                        f'Invalid thinking level "{invalid_level}" in pattern "{raw_pattern}". Using default instead.'
                    )
                    resolved = fallback
                    pattern = base_pattern
            if not resolved:
                warnings.append(f'No models match pattern "{raw_pattern}"')
                continue
            effective_thinking = thinking or default_thinking
            for provider, model in resolved:
                key = (provider, model)
                if key in seen:
                    continue
                seen.add(key)
                matched.append((provider, model, effective_thinking))
        return matched, warnings

    def _resolve_scoped_models(self) -> list[tuple[str, str, str | None]]:
        matched, _warnings = self._resolve_scoped_models_with_warnings()
        return matched

    def _is_model_alias(self, model_id: str) -> bool:
        return model_id.endswith("-latest") or re.search(r"-\d{8}$", model_id) is None

    def list_available_models(self, search: str | None = None) -> list[str]:
        catalog = self._available_model_catalog()
        models = [f"{provider}/{model}" for provider, items in catalog.items() for model in items]
        if not search:
            return models
        needle = search.strip().lower()
        if not needle:
            return models
        return [m for m in models if needle in m.lower()]

    def _resolve_provider_and_model(self, provider: str | None, model: str | None) -> tuple[str, str]:
        catalog = self._available_model_catalog()
        all_models = [(p, m) for p, models in catalog.items() for m in models]

        explicit_provider = provider
        model_pattern = model
        if model and "/" in model and not provider:
            pfx, model_id = model.split("/", 1)
            if pfx in catalog:
                explicit_provider = pfx
                model_pattern = model_id
            else:
                return pfx, model_id

        if explicit_provider:
            provider_name = explicit_provider
        elif self.settings.default_provider and self.settings.default_provider in catalog:
            provider_name = self.settings.default_provider
        elif "openai" in catalog:
            provider_name = "openai"
        else:
            provider_name = next(iter(catalog), "openai")
        if model_pattern:
            candidates = (
                [(provider_name, m) for m in catalog.get(provider_name, [])]
                if explicit_provider
                else all_models
            )
            resolved = self._resolve_model_pattern(model_pattern, candidates)
            if resolved:
                return resolved[0]
            return provider_name, model_pattern

        if self.settings.default_model:
            resolved = self._resolve_model_pattern(self.settings.default_model, all_models)
            if resolved:
                return resolved[0]

        provider_models = catalog.get(provider_name, [])
        if provider_models:
            return provider_name, provider_models[0]

        if all_models:
            return all_models[0]
        return provider_name, self.settings.default_model or "gpt-4o-mini"

    def _split_model_thinking(self, model: str | None) -> tuple[str | None, str | None]:
        if not model or ":" not in model:
            return model, None
        candidate_model, candidate_level = model.rsplit(":", 1)
        if candidate_level in {"off", "minimal", "low", "medium", "high", "xhigh"} and candidate_model:
            return candidate_model, candidate_level
        return model, None

    def _model_supports_reasoning(self, provider: str, model_id: str) -> bool:
        definition = self.model_registry.get_model_definition(provider, model_id)
        if definition is None:
            return True
        if definition.reasoning is False:
            return False
        return True

    def _clamp_thinking_for_current_model(self) -> None:
        if not self._model_supports_reasoning(self.provider_name, self.model_id):
            self.thinking_level = "off"

    def get_messages(self) -> list[AgentMessage]:
        return self.session_manager.build_context().messages

    def get_state(self) -> dict[str, Any]:
        header = self.session_manager.header
        return {
            "provider": self.provider_name,
            "modelId": self.model_id,
            "thinkingLevel": self.thinking_level,
            "isStreaming": False,
            "isCompacting": False,
            "steeringMode": self.steering_mode,
            "followUpMode": self.follow_up_mode,
            "sessionFile": self.session_file,
            "sessionId": header.id if header else None,
            "sessionName": self.session_manager.get_session_name(),
            "autoCompactionEnabled": self.settings.compaction.enabled,
            "messageCount": len(self.session_manager.build_context().messages),
            "pendingMessageCount": len(self._steering_queue) + len(self._follow_up_queue),
            "steeringQueueCount": len(self._steering_queue),
            "followUpQueueCount": len(self._follow_up_queue),
            "tools": self.available_tools,
            "extensionFlags": dict(self.extension_flags),
        }

    def _build_aborted_assistant(self, message: str = "Request was aborted") -> AssistantMessage:
        return AssistantMessage(
            content=[],
            provider=self.provider_name,
            model=self.model_id,
            stopReason="aborted",
            errorMessage=message,
        )

    def _emit_aborted_turn(self, assistant: AssistantMessage) -> None:
        self._emit(MessageStart(message=assistant))
        self._emit(MessageUpdate(message=assistant, assistantMessageEvent=AssistantMessageEvent(type="start")))
        self._emit(
            MessageUpdate(
                message=assistant,
                assistantMessageEvent=AssistantMessageEvent(type="error", error=assistant.error_message or "aborted"),
            )
        )
        self._emit(MessageUpdate(message=assistant, assistantMessageEvent=AssistantMessageEvent(type="done")))
        self._emit(MessageEnd(message=assistant))
        self._emit(TurnEnd(message=assistant, toolResults=[]))
        self._emit(AgentEnd(messages=[assistant]))

    def steer(self, message: str, images: list[ImageContent] | None = None) -> None:
        expanded = self._expand_user_prompt(message)
        self._steering_queue.append(self._build_user_message(expanded, images or []))

    def follow_up(self, message: str, images: list[ImageContent] | None = None) -> None:
        expanded = self._expand_user_prompt(message)
        self._follow_up_queue.append(self._build_user_message(expanded, images or []))

    def _dequeue_steering(self) -> list[AgentMessage]:
        if self.steering_mode == "one-at-a-time":
            if not self._steering_queue:
                return []
            return [self._steering_queue.pop(0)]
        items = self._steering_queue[:]
        self._steering_queue.clear()
        return items

    def _dequeue_follow_up(self) -> list[AgentMessage]:
        if self.follow_up_mode == "one-at-a-time":
            if not self._follow_up_queue:
                return []
            return [self._follow_up_queue.pop(0)]
        items = self._follow_up_queue[:]
        self._follow_up_queue.clear()
        return items

    def _build_user_message(self, message: str, images: list[ImageContent]) -> UserMessage:
        if not images:
            return UserMessage(content=message)
        blocks: list[TextContent | ImageContent] = [TextContent(text=message), *images]
        return UserMessage(content=blocks)

    def _build_system_prompt(self) -> str:
        context_files = self.resource_loader.state.context_files
        skills = self.resource_loader.state.skills
        selected_tools = list(self.tool_registry.tools.keys())
        return build_system_prompt(
            cwd=self.cwd,
            custom_prompt=self._system_prompt_override,
            selected_tools=selected_tools,
            append_system_prompt=self._append_system_prompt,
            context_files=context_files,
            skills=skills,
        )

    async def _provider_call(self, messages: list[AgentMessage]) -> AssistantMessage:
        self.model_registry.refresh()
        api_key = self.model_registry.get_api_key_for_provider(
            self.provider_name,
            cli_api_key=self.cli_api_key,
            cli_provider=self.cli_api_key_provider,
        )
        if not api_key:
            return AssistantMessage(
                content=[
                    TextContent(
                        text=(
                            f"No API key for provider {self.provider_name}. "
                            "Set CLI --api-key, auth.json, environment variable, or models.json provider.apiKey."
                        )
                    )
                ],
                provider=self.provider_name,
                model=self.model_id,
                stopReason="error",
                errorMessage="missing_api_key",
            )

        runtime_model = self.model_registry.find_model(self.provider_name, self.model_id)
        resolved_base_url = runtime_model.base_url if runtime_model else None
        if self.cli_base_url and self.cli_base_url_provider == self.provider_name:
            resolved_base_url = self.cli_base_url
        resolved_headers = runtime_model.headers if runtime_model else None

        transport_provider = self.model_registry.resolve_transport_provider(self.provider_name, self.model_id)
        provider = self.provider_registry.get(transport_provider)
        tools = list(self.tool_registry.tools.values())
        request = ProviderRequest(
            provider=self.provider_name,
            model_id=self.model_id,
            api_key=api_key,
            system_prompt=self._build_system_prompt(),
            messages=messages,
            tools=tools,
            thinking_level=self.thinking_level,
            base_url=resolved_base_url,
            headers=resolved_headers,
        )
        return await provider.complete(request)

    async def _provider_stream_call(self, messages: list[AgentMessage]) -> AsyncIterator[ProviderStreamEvent]:
        self.model_registry.refresh()
        api_key = self.model_registry.get_api_key_for_provider(
            self.provider_name,
            cli_api_key=self.cli_api_key,
            cli_provider=self.cli_api_key_provider,
        )
        if not api_key:
            missing = AssistantMessage(
                content=[
                    TextContent(
                        text=(
                            f"No API key for provider {self.provider_name}. "
                            "Set CLI --api-key, auth.json, environment variable, or models.json provider.apiKey."
                        )
                    )
                ],
                provider=self.provider_name,
                model=self.model_id,
                stopReason="error",
                errorMessage="missing_api_key",
            )
            async for item in stream_events_from_assistant(missing):
                yield item
            return

        runtime_model = self.model_registry.find_model(self.provider_name, self.model_id)
        resolved_base_url = runtime_model.base_url if runtime_model else None
        if self.cli_base_url and self.cli_base_url_provider == self.provider_name:
            resolved_base_url = self.cli_base_url
        resolved_headers = runtime_model.headers if runtime_model else None

        transport_provider = self.model_registry.resolve_transport_provider(self.provider_name, self.model_id)
        provider = self.provider_registry.get(transport_provider)
        request = ProviderRequest(
            provider=self.provider_name,
            model_id=self.model_id,
            api_key=api_key,
            system_prompt=self._build_system_prompt(),
            messages=messages,
            tools=list(self.tool_registry.tools.values()),
            thinking_level=self.thinking_level,
            base_url=resolved_base_url,
            headers=resolved_headers,
        )
        stream_method = getattr(provider, "stream_complete", None)
        if callable(stream_method):
            async for item in stream_method(request):
                yield item
            return

        fallback = await provider.complete(request)
        async for item in stream_events_from_assistant(fallback):
            yield item

    async def _execute_tool(self, name: str, args: dict[str, Any]) -> tuple[list[UserContentBlock], Any | None, bool]:
        return await self.tool_registry.execute(name, args)

    def _models_with_auth(self, models: list[tuple[str, str, str | None]]) -> list[tuple[str, str, str | None]]:
        out: list[tuple[str, str, str | None]] = []
        for provider, model, thinking in models:
            key = self.model_registry.get_api_key_for_provider(
                provider,
                cli_api_key=self.cli_api_key,
                cli_provider=self.cli_api_key_provider,
            )
            if key:
                out.append((provider, model, thinking))
        return out

    def _sync_runtime_from_session_context(self) -> None:
        if not self.session_manager.entries:
            return
        context = self.session_manager.build_context()
        model = context.model
        if model and model.get("provider") and model.get("modelId"):
            self.provider_name = str(model["provider"])
            self.model_id = str(model["modelId"])
        if context.thinking_level:
            self.thinking_level = context.thinking_level
        self._clamp_thinking_for_current_model()

    def _expand_skill_command(self, text: str) -> str:
        if not text.startswith("/skill:"):
            return text
        if not self._skill_commands_enabled:
            return text

        command_part, _, args = text.partition(" ")
        skill_name = command_part[7:]
        skill = next((s for s in self.resource_loader.state.skills if s.name == skill_name), None)
        if not skill:
            return text
        try:
            raw = Path(skill.file_path).read_text(encoding="utf-8")
            _meta, body = parse_frontmatter(raw)
            body = body.strip()
            skill_block = (
                f'<skill name="{skill.name}" location="{skill.file_path}">\n'
                f"References are relative to {skill.base_dir}.\n\n"
                f"{body}\n"
                "</skill>"
            )
            suffix = args.strip()
            return f"{skill_block}\n\n{suffix}" if suffix else skill_block
        except Exception:
            return text

    def _expand_user_prompt(self, text: str) -> str:
        expanded = self._expand_skill_command(text)
        return self.resource_loader.expand_prompt(expanded)

    def _parse_setting_value(self, raw: str) -> Any:
        lowered = raw.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        if lowered in {"null", "none"}:
            return None
        try:
            if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
                return int(raw)
            return float(raw)
        except ValueError:
            pass
        try:
            return json.loads(raw)
        except Exception:
            return raw

    def _dict_get_nested(self, data: dict[str, Any], path: str) -> Any:
        cur: Any = data
        for key in path.split("."):
            if not isinstance(cur, dict):
                return None
            if key in cur:
                cur = cur[key]
            elif key in {k.replace("-", "_") for k in cur}:
                mapped = next(k for k in cur if k.replace("-", "_") == key)
                cur = cur[mapped]
            else:
                return None
        return cur

    def _dict_set_nested(self, data: dict[str, Any], path: str, value: Any) -> None:
        parts = path.split(".")
        cur = data
        for key in parts[:-1]:
            if key not in cur or not isinstance(cur[key], dict):
                cur[key] = {}
            cur = cur[key]
        cur[parts[-1]] = value

    def _handle_settings_command(self, rest: str) -> str:
        if not rest:
            return self.settings.model_dump_json(indent=2, by_alias=True)
        try:
            tokens = shlex.split(rest)
        except ValueError as exc:
            return f"Invalid /settings syntax: {exc}"
        if not tokens:
            return self.settings.model_dump_json(indent=2, by_alias=True)

        op = tokens[0]
        if op == "get":
            if len(tokens) < 2:
                return "Usage: /settings get <key>"
            key = tokens[1]
            data = self.settings.model_dump(by_alias=True, exclude_none=False)
            value = self._dict_get_nested(data, key)
            return f"{key} = {value!r}"
        if op == "set":
            if len(tokens) < 3:
                return "Usage: /settings set <key> <value> [global|project]"
            key = tokens[1]
            value = self._parse_setting_value(tokens[2])
            scope = tokens[3] if len(tokens) > 3 else "project"
            scope = "project" if scope.lower() == "project" else "global"
            target = self.global_settings if scope == "global" else self.project_settings
            dumped = target.model_dump(by_alias=True, exclude_none=False)
            self._dict_set_nested(dumped, key, value)
            validated = target.model_validate(dumped)
            if scope == "global":
                self.global_settings = validated
            else:
                self.project_settings = validated
            save_settings(self.cwd, validated, scope=scope)
            self.global_settings, self.project_settings, self.settings = load_settings(self.cwd)
            return f"Updated {scope} setting: {key}={value!r}"
        return "Usage: /settings [get|set]"

    def _handle_manual_compact(self) -> str:
        context = self.session_manager.build_context().messages
        if not context or not self.session_manager.entries:
            return "No session context to compact."
        summary = generate_compaction_summary(context)
        first_kept_entry_id = self._select_compaction_anchor_id(self.settings.compaction.keep_recent_tokens)
        est_tokens = len(summary) // 4
        self.session_manager.append_compaction(summary, first_kept_entry_id, est_tokens)
        compact_msg = build_compaction_message(summary, est_tokens)
        self.session_manager.append_message(compact_msg)
        return "Manual compaction completed."

    def _select_compaction_anchor_id(self, keep_recent_tokens: int) -> str:
        branch = self.session_manager.get_branch()
        if not branch:
            return self.session_manager.entries[max(0, len(self.session_manager.entries) // 2)].id

        budget = max(1, keep_recent_tokens)
        running = 0
        anchor = branch[0].id
        for entry in reversed(branch):
            anchor = entry.id
            if entry.type == "message":
                running += estimate_message_tokens([entry.message])
            elif entry.type == "branch_summary":
                running += max(1, len(entry.summary) // 4)
            elif entry.type == "compaction":
                running += max(1, len(entry.summary) // 4)
            elif entry.type == "custom":
                running += max(1, len(str(getattr(entry, "data", ""))) // 4)
            if running >= budget:
                break
        return anchor

    def _handle_tree_command(self, rest: str) -> str:
        indexed_entries = self.session_manager.entries[-50:]
        if rest:
            target = rest.strip()
            if target in {"root", "none"}:
                self.session_manager.set_leaf(None)
                return "Moved to root (empty context)."
            if target.isdigit():
                index = int(target) - 1
                if 0 <= index < len(indexed_entries):
                    entry = indexed_entries[index]
                    self.session_manager.set_leaf(entry.id)
                    return f"Moved tree leaf to #{index + 1} ({entry.id})."
                return f"Invalid tree index: {target}"
            ok = self.session_manager.set_leaf(target)
            if not ok:
                return f"Unknown entry id: {target}"
            return f"Moved tree leaf to {target}."

        lines = []
        leaf = self.session_manager.leaf_id
        for idx, entry in enumerate(indexed_entries, start=1):
            mark = "*" if entry.id == leaf else " "
            lines.append(f"{mark} #{idx:02d} {entry.id} {entry.type} parent={entry.parent_id}")
        if not lines:
            return "(empty tree)"
        return "Tree entries (use /tree <index|entry_id|root>):\n" + "\n".join(lines)

    def _handle_fork_command(self, rest: str) -> str:
        leaf = rest.strip() if rest.strip() else None
        if leaf and leaf not in self.session_manager.by_id:
            return f"Unknown entry id: {leaf}"
        new_file = self.fork_session(leaf_id=leaf)
        return f"Forked session to {new_file}"

    def _handle_resume_command(self, rest: str) -> str:
        arg = rest.strip()
        sessions = self.session_manager.list_sessions(limit=20)
        if not arg:
            if not sessions:
                return "No previous sessions found."
            lines = []
            current_file = self.session_file
            for idx, summary in enumerate(sessions, start=1):
                title = summary.session_name or summary.first_user_message or "(no title)"
                mark = "*" if current_file and summary.path == current_file else " "
                lines.append(f"{mark} {idx}. {summary.path} | messages={summary.message_count} | {title}")
            return "Recent sessions:\n" + "\n".join(lines)

        target_path = None
        if arg.isdigit():
            index = int(arg) - 1
            if 0 <= index < len(sessions):
                target_path = sessions[index].path
        else:
            candidate = Path(arg).expanduser()
            if not candidate.is_absolute():
                candidate = self.session_manager.session_dir / arg
            target_path = str(candidate.resolve())

        if not target_path:
            return "Invalid /resume target. Use /resume to list or /resume <index|path>."
        self.session_manager.switch_session_file(target_path)
        self._sync_runtime_from_session_context()
        return f"Resumed session: {target_path}"

    def _handle_scoped_models_command(self, rest: str) -> str:
        arg = rest.strip()
        if not arg:
            if not self._scoped_model_patterns:
                return "Scoped models disabled. Using all known models."
            return "Scoped patterns: " + ", ".join(self._scoped_model_patterns)
        if arg in {"clear", "off"}:
            self.set_scoped_models([])
            return "Scoped models cleared."
        patterns = [part.strip() for part in arg.split(",") if part.strip()]
        resolved = self.set_scoped_models(patterns)
        if not resolved:
            if self._last_model_scope_warnings:
                return "\n".join(["Scoped models updated: (no matches)", *self._last_model_scope_warnings])
            return "Scoped models updated: (no matches)"
        lines = ["Scoped models updated:", *resolved]
        if self._last_model_scope_warnings:
            lines.extend(["", *self._last_model_scope_warnings])
        return "\n".join(lines)

    def list_sessions(
        self,
        limit: int = 20,
        offset: int = 0,
        include_current: bool = True,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, limit)
        safe_offset = max(0, offset)
        requested = safe_limit + safe_offset + (1 if not include_current else 0)
        sessions = [
            {
                "path": s.path,
                "modified": s.modified,
                "messageCount": s.message_count,
                "firstMessage": s.first_user_message,
                "name": s.session_name,
            }
            for s in self.session_manager.list_sessions(limit=requested)
        ]
        if not include_current:
            current = self.session_file
            sessions = [row for row in sessions if row["path"] != current]
        if safe_offset:
            sessions = sessions[safe_offset:]
        return sessions[:safe_limit]

    def get_tree(self, limit: int | None = None, include_root: bool = False) -> dict[str, Any]:
        entries = self.session_manager.get_tree_entries()
        if limit is not None:
            safe_limit = max(1, limit)
            entries = entries[-safe_limit:]
        if include_root:
            entries = [
                {
                    "id": None,
                    "parentId": None,
                    "type": "root",
                    "timestamp": None,
                },
                *entries,
            ]
        return {
            "leafId": self.session_manager.leaf_id,
            "entries": entries,
        }

    def switch_tree(self, leaf_id: str | None) -> bool:
        return self.session_manager.set_leaf(leaf_id)

    def resume_session(self, target: str | int) -> str:
        if isinstance(target, int):
            sessions = self.session_manager.list_sessions(limit=50)
            index = target - 1
            if index < 0 or index >= len(sessions):
                raise ValueError(f"Invalid session index: {target}")
            path = sessions[index].path
        else:
            path_obj = Path(target).expanduser()
            if not path_obj.is_absolute():
                path_obj = self.session_manager.session_dir / target
            path = str(path_obj.resolve())
        self.session_manager.switch_session_file(path)
        self._sync_runtime_from_session_context()
        return path

    def fork_session(self, leaf_id: str | None = None) -> str | None:
        if leaf_id is not None and leaf_id not in self.session_manager.by_id:
            return None
        source_leaf = leaf_id if leaf_id is not None else self.session_manager.leaf_id
        source_messages = self.session_manager.build_context(leaf_id=source_leaf).messages if source_leaf else []
        summary_text = generate_compaction_summary(source_messages, max_messages=8) if source_messages else None

        new_file = self.session_manager.fork_current_branch(leaf_id=leaf_id)
        if source_leaf and summary_text:
            self.session_manager.append_branch_summary(summary_text, source_leaf)
        return str(new_file) if new_file else None

    def compact_now(self) -> str:
        return self._handle_manual_compact()

    def reload_resources(self) -> dict[str, list[str]]:
        state = self.resource_loader.reload(
            extra_skill_paths=self._extra_skill_paths,
            extra_prompt_paths=self._extra_prompt_paths,
            extra_theme_paths=self._extra_theme_paths,
            include_discovered_skills=self._include_discovered_skills,
            include_discovered_prompts=self._include_discovered_prompts,
            include_discovered_themes=self._include_discovered_themes,
        )
        self.extension_runner.load(self._extension_paths)
        self._rebuild_tool_registry()
        return {
            "skills": state.diagnostics.skills,
            "prompts": state.diagnostics.prompts,
            "themes": state.diagnostics.themes,
            "extensions": list(self.extension_runner.errors),
        }

    def set_steering_mode(self, mode: str) -> None:
        if mode not in {"all", "one-at-a-time"}:
            raise ValueError("steering mode must be all or one-at-a-time")
        self.steering_mode = mode

    def set_follow_up_mode(self, mode: str) -> None:
        if mode not in {"all", "one-at-a-time"}:
            raise ValueError("follow-up mode must be all or one-at-a-time")
        self.follow_up_mode = mode

    def set_thinking_level(self, level: str) -> None:
        if level not in {"off", "minimal", "low", "medium", "high", "xhigh"}:
            raise ValueError("invalid thinking level")
        effective = level
        if not self._model_supports_reasoning(self.provider_name, self.model_id):
            effective = "off"
        if effective == self.thinking_level:
            return
        self.thinking_level = effective
        self.session_manager.append_thinking_level(effective)

    def set_session_name(self, name: str) -> None:
        self.session_manager.set_session_name(name)

    def set_scoped_models(self, patterns: list[str]) -> list[str]:
        cleaned = [p.strip() for p in patterns if p.strip()]
        self._scoped_model_patterns = cleaned
        self.project_settings.enabled_models = cleaned
        save_settings(self.cwd, self.project_settings, scope="project")
        resolved_models, warnings = self._resolve_scoped_models_with_warnings()
        self._last_model_scope_warnings = warnings
        resolved: list[str] = []
        for provider, model, thinking in resolved_models:
            token = f"{provider}/{model}"
            if thinking:
                token += f":{thinking}"
            resolved.append(token)
        return resolved

    async def prompt(
        self,
        message: str,
        images: list[ImageContent] | None = None,
        streaming_behavior: str | None = None,
    ) -> list[AgentMessage]:
        if streaming_behavior == "steer":
            self.steer(message, images)
            return []
        if streaming_behavior == "followUp":
            self.follow_up(message, images)
            return []

        expanded = self._expand_user_prompt(message)
        handled, response = await self.command_router.handle(expanded)
        if handled:
            reply = AssistantMessage(
                content=[TextContent(text=response or "")],
                provider="system",
                model="gen",
            )
            self.session_manager.append_message(reply)
            return [reply]

        user_message = self._build_user_message(expanded, images or [])
        context = self.session_manager.build_context().messages

        compaction = should_compact(
            context,
            reserve_tokens=self.settings.compaction.reserve_tokens,
            keep_recent_tokens=self.settings.compaction.keep_recent_tokens,
        )
        if self.settings.compaction.enabled and compaction.should_compact and self.session_manager.entries:
            self._emit(AutoCompactionStart(reason=compaction.reason or "threshold"))
            summary = generate_compaction_summary(context)
            first_kept_entry_id = self._select_compaction_anchor_id(self.settings.compaction.keep_recent_tokens)
            self.session_manager.append_compaction(summary, first_kept_entry_id, compaction.estimated_tokens)
            compact_msg = build_compaction_message(summary, compaction.estimated_tokens)
            self.session_manager.append_message(compact_msg)
            self._emit(AutoCompactionEnd(result={"summary": summary}, aborted=False, willRetry=False))
            context = self.session_manager.build_context().messages

        new_messages = await self.run_executor.run(prompts=[user_message], context=context)
        for msg in new_messages:
            self.session_manager.append_message(msg)

        self.extension_runner.emit(
            "agent_end",
            {"messages": [m.model_dump(by_alias=True) for m in new_messages]},
            self,
        )
        return new_messages

    async def continue_run(self) -> list[AgentMessage]:
        context = self.session_manager.build_context().messages
        new_messages = await self.run_executor.run([], context)
        for msg in new_messages:
            self.session_manager.append_message(msg)
        self.extension_runner.emit(
            "agent_end",
            {"messages": [m.model_dump(by_alias=True) for m in new_messages]},
            self,
        )
        return new_messages

    def set_model(self, provider: str, model_id: str) -> None:
        self.provider_name = provider
        self.model_id = model_id
        self.session_manager.append_model_change(provider, model_id)
        self.set_thinking_level(self.thinking_level)

    def apply_scoped_startup_model(self) -> bool:
        scoped = self._resolve_scoped_models()
        scoped_with_auth = self._models_with_auth(scoped)
        if scoped_with_auth:
            scoped = scoped_with_auth
        if not scoped:
            return False
        current = (self.provider_name, self.model_id)
        provider_model_pairs = [(provider, model) for provider, model, _thinking in scoped]
        if current in provider_model_pairs:
            idx = provider_model_pairs.index(current)
            scoped_thinking = scoped[idx][2]
            if scoped_thinking:
                self.thinking_level = scoped_thinking
            return False
        self.provider_name, self.model_id, scoped_thinking = scoped[0]
        if scoped_thinking:
            self.thinking_level = scoped_thinking
        return True

    def cycle_model(self, direction: str = "forward") -> dict[str, str | bool]:
        scoped = self._resolve_scoped_models()
        scoped_with_auth = self._models_with_auth(scoped)
        if scoped_with_auth:
            scoped = scoped_with_auth
        if not scoped:
            scoped = [(self.provider_name, self.model_id, None)]
        current = (self.provider_name, self.model_id)
        provider_model_pairs = [(provider, model) for provider, model, _thinking in scoped]
        step = -1 if direction == "backward" else 1
        if current not in provider_model_pairs:
            self.provider_name, self.model_id, scoped_thinking = scoped[0]
        else:
            idx = (provider_model_pairs.index(current) + step) % len(scoped)
            self.provider_name, self.model_id, scoped_thinking = scoped[idx]
        self.session_manager.append_model_change(self.provider_name, self.model_id)
        if scoped_thinking:
            self.set_thinking_level(scoped_thinking)
        else:
            self.set_thinking_level(self.thinking_level)
        return {
            "provider": self.provider_name,
            "modelId": self.model_id,
            "thinkingLevel": self.thinking_level,
            "isScoped": bool(self._scoped_model_patterns),
        }

    def new_session(self, parent_session: str | None = None) -> None:
        self.session_manager.new_session(parent_session=parent_session)
