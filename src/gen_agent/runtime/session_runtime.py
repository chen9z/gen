from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from gen_agent.core.auth_store import AuthStore
from gen_agent.core.compaction import generate_compaction_summary
from gen_agent.core.model_registry import ModelRegistry
from gen_agent.core.session_manager import SessionManager
from gen_agent.core.settings_store import load_settings
from gen_agent.core.system_prompt import build_system_prompt
from gen_agent.extensions import ExtensionUIContext, ExtensionRunner, NoOpExtensionUIContext
from gen_agent.models.content import ImageContent, TextContent, UserContentBlock
from gen_agent.models.events import (
    AgentEvent,
    AgentSessionEvent,
    AutoCompactionEnd,
    AutoCompactionStart,
)
from gen_agent.models.messages import AgentMessage, AssistantMessage
from gen_agent.providers import ProviderRegistry
from gen_agent.providers.stream_types import ProviderStreamEvent
from gen_agent.resources import ResourceLoader
from gen_agent.tools import DEFAULT_TOOL_NAMES, ToolRegistry, create_all_tools

from .commands import CommandResult, build_command_registry
from .compaction_service import CompactionService
from .event_emitter import EventEmitter
from .model_controller import ModelController
from .prompt_pipeline import PromptPipeline
from .provider_runtime import ProviderRuntime
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
    ) -> None:
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

        self.resource_loader.reload(
            extra_skill_paths=self._extra_skill_paths,
            extra_prompt_paths=self._extra_prompt_paths,
            extra_theme_paths=self._extra_theme_paths,
            include_discovered_skills=self._include_discovered_skills,
            include_discovered_prompts=self._include_discovered_prompts,
            include_discovered_themes=self._include_discovered_themes,
        )
        self.extension_runner.load(self._extension_paths)

        self.session_manager = SessionManager(
            cwd=self.cwd,
            persist=persist_session,
            session_file=session_file,
            session_dir=session_dir,
        )

        self._core_tools = self._build_core_tools(tools)
        self.tool_registry = ToolRegistry(self._core_tools + list(self.extension_runner.get_tools().values()))

        self._steering_queue: list[AgentMessage] = []
        self._follow_up_queue: list[AgentMessage] = []
        self.steering_mode = self.settings.steering_mode
        self.follow_up_mode = self.settings.follow_up_mode

        self.model_controller = ModelController(
            cwd=self.cwd,
            model_registry=self.model_registry,
            session_manager=self.session_manager,
            settings=self.settings,
            project_settings=self.project_settings,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            cli_api_key=api_key,
            cli_api_key_provider=None,
        )
        startup_provider = self.model_controller.provider_name
        self.model_controller.set_cli_provider_scope(startup_provider if api_key else None)
        self.model_controller.sync_from_session_context()

        self.cli_api_key = api_key
        self.cli_api_key_provider = startup_provider if api_key else None
        self.cli_base_url = base_url
        self.cli_base_url_provider = startup_provider if base_url else None

        self.event_emitter = EventEmitter(self)
        self.prompt_pipeline = PromptPipeline(
            resource_loader=self.resource_loader,
            skill_commands_enabled=self._skill_commands_enabled,
        )
        self.provider_runtime = ProviderRuntime(
            provider_registry=self.provider_registry,
            model_registry=self.model_registry,
            model_controller=self.model_controller,
            tool_registry_getter=lambda: self.tool_registry,
            system_prompt_getter=self._build_system_prompt,
            cli_api_key=self.cli_api_key,
            cli_api_key_provider=self.cli_api_key_provider,
            cli_base_url=self.cli_base_url,
            cli_base_url_provider=self.cli_base_url_provider,
        )
        self.compaction_service = CompactionService(
            session_manager=self.session_manager,
            settings_getter=lambda: self.settings.compaction,
        )
        self.command_registry = build_command_registry(
            cwd=self.cwd,
            global_settings_getter=lambda: self.global_settings,
            project_settings_getter=lambda: self.project_settings,
            settings_getter=lambda: self.settings,
            on_settings_updated=self._apply_settings_update,
            extension_commands_getter=self.extension_runner.get_commands,
            runtime_context_getter=lambda: self,
            session_ops=self,
            model_controller=self.model_controller,
            compaction_service=self.compaction_service,
            reload_resources=self.reload_resources,
        )
        self.run_executor = RunExecutor(
            provider_call=self._provider_call,
            provider_stream_call=self._provider_stream_call,
            exec_tool=self._execute_tool,
            emit=self._emit,
            event_emitter=self.event_emitter,
            get_steering_messages=self._dequeue_steering,
            get_follow_up_messages=self._dequeue_follow_up,
            provider_name_getter=lambda: self.provider_name,
            model_id_getter=lambda: self.model_id,
            retry_settings_getter=lambda: self.settings.retry,
        )

    @property
    def provider_name(self) -> str:
        return self.model_controller.provider_name

    @property
    def model_id(self) -> str:
        return self.model_controller.model_id

    @property
    def thinking_level(self) -> str:
        return self.model_controller.thinking_level

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
        self.ui = context if self.ui_extensions_enabled and context is not None else NoOpExtensionUIContext()

    def subscribe(self, listener):
        return self.event_emitter.subscribe(listener)

    def _emit(self, event: AgentSessionEvent | AgentEvent) -> AgentSessionEvent:
        return self.event_emitter.emit(event)

    def _build_core_tools(self, tools: list[str] | None) -> list[Any]:
        all_tools = create_all_tools(self.cwd, shell_command_prefix=self.settings.shell_command_prefix)
        enabled_names = tools or DEFAULT_TOOL_NAMES
        return [all_tools[name] for name in enabled_names if name in all_tools]

    def _rebuild_tool_registry(self) -> None:
        self.tool_registry = ToolRegistry(self._core_tools + list(self.extension_runner.get_tools().values()))

    def _build_system_prompt(self) -> str:
        return build_system_prompt(
            cwd=self.cwd,
            custom_prompt=self._system_prompt_override,
            selected_tools=list(self.tool_registry.tools.keys()),
            append_system_prompt=self._append_system_prompt,
            context_files=self.resource_loader.state.context_files,
            skills=self.resource_loader.state.skills,
        )

    def _apply_settings_update(self, global_settings, project_settings, merged_settings) -> None:
        self.global_settings = global_settings
        self.project_settings = project_settings
        self.settings = merged_settings
        self._skill_commands_enabled = self.settings.enable_skill_commands and self._include_discovered_skills
        self.prompt_pipeline.update_skill_commands_enabled(self._skill_commands_enabled)
        self.model_controller.update_settings(self.settings, self.project_settings)
        if not self.ui_extensions_enabled:
            self.ui = NoOpExtensionUIContext()

    def list_available_models(self, search: str | None = None) -> list[str]:
        self.model_registry.refresh()
        models = [
            f"{provider}/{model}"
            for provider, items in self.model_registry.load_catalog().items()
            for model in items
        ]
        if not search or not search.strip():
            return models
        needle = search.strip().lower()
        return [item for item in models if needle in item.lower()]

    def get_messages(self) -> list[AgentMessage]:
        return self.session_manager.build_context().messages

    def get_state(self) -> dict[str, Any]:
        header = self.session_manager.header
        steering_count = len(self._steering_queue)
        follow_up_count = len(self._follow_up_queue)
        return {
            "provider": self.model_controller.provider_name,
            "modelId": self.model_controller.model_id,
            "thinkingLevel": self.model_controller.thinking_level,
            "isStreaming": False,
            "isCompacting": False,
            "steeringMode": self.steering_mode,
            "followUpMode": self.follow_up_mode,
            "sessionFile": str(self.session_manager.file) if self.session_manager.file else None,
            "sessionId": header.id if header else None,
            "sessionName": self.session_manager.get_session_name(),
            "autoCompactionEnabled": self.settings.compaction.enabled,
            "messageCount": len(self.session_manager.build_context().messages),
            "pendingMessageCount": steering_count + follow_up_count,
            "steeringQueueCount": steering_count,
            "followUpQueueCount": follow_up_count,
            "tools": self.available_tools,
            "extensionFlags": dict(self.extension_flags),
        }

    def steer(self, message: str, images: list[ImageContent] | None = None) -> None:
        expanded = self.prompt_pipeline.expand_prompt(message)
        self._steering_queue.append(self.prompt_pipeline.build_user_message(expanded, images or []))

    def follow_up(self, message: str, images: list[ImageContent] | None = None) -> None:
        expanded = self.prompt_pipeline.expand_prompt(message)
        self._follow_up_queue.append(self.prompt_pipeline.build_user_message(expanded, images or []))

    def _dequeue_steering(self) -> list[AgentMessage]:
        if self.steering_mode == "one-at-a-time":
            return [self._steering_queue.pop(0)] if self._steering_queue else []
        items = self._steering_queue[:]
        self._steering_queue.clear()
        return items

    def _dequeue_follow_up(self) -> list[AgentMessage]:
        if self.follow_up_mode == "one-at-a-time":
            return [self._follow_up_queue.pop(0)] if self._follow_up_queue else []
        items = self._follow_up_queue[:]
        self._follow_up_queue.clear()
        return items

    async def _provider_call(self, messages: list[AgentMessage]) -> AssistantMessage:
        return await self.provider_runtime.complete(messages)

    async def _provider_stream_call(self, messages: list[AgentMessage]) -> AsyncIterator[ProviderStreamEvent]:
        async for item in self.provider_runtime.stream(messages):
            yield item

    async def _execute_tool(self, name: str, args: dict[str, Any]) -> tuple[list[UserContentBlock], Any | None, bool]:
        return await self.tool_registry.execute(name, args)

    def list_sessions(self, limit: int = 20, offset: int = 0, include_current: bool = True) -> list[dict[str, Any]]:
        safe_limit = max(1, limit)
        safe_offset = max(0, offset)
        requested = safe_limit + safe_offset + (1 if not include_current else 0)
        sessions = [
            {
                "path": item.path,
                "modified": item.modified,
                "messageCount": item.message_count,
                "firstMessage": item.first_user_message,
                "name": item.session_name,
            }
            for item in self.session_manager.list_sessions(limit=requested)
        ]
        if not include_current:
            current = str(self.session_manager.file) if self.session_manager.file else None
            sessions = [row for row in sessions if row["path"] != current]
        if safe_offset:
            sessions = sessions[safe_offset:]
        return sessions[:safe_limit]

    def get_tree(self, limit: int | None = None, include_root: bool = False) -> dict[str, Any]:
        entries = self.session_manager.get_tree_entries()
        if limit is not None:
            entries = entries[-max(1, limit):]
        if include_root:
            entries = [{"id": None, "parentId": None, "type": "root", "timestamp": None}, *entries]
        return {"leafId": self.session_manager.leaf_id, "entries": entries}

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
        self.model_controller.sync_from_session_context()
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
        return self.compaction_service.compact_now()

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
        self.model_controller.set_thinking_level(level)

    def set_session_name(self, name: str) -> None:
        self.session_manager.set_session_name(name)

    def set_scoped_models(self, patterns: list[str]) -> list[str]:
        return self.model_controller.set_scoped_models(patterns)

    def set_model(self, provider: str, model_id: str) -> None:
        self.model_controller.set_model(provider, model_id)

    def apply_scoped_startup_model(self) -> bool:
        return self.model_controller.apply_scoped_startup_model()

    def cycle_model(self, direction: str = "forward") -> dict[str, str | bool]:
        return self.model_controller.cycle_model(direction=direction)

    def new_session(self, parent_session: str | None = None) -> None:
        self.session_manager.new_session(parent_session=parent_session)

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

        expanded = self.prompt_pipeline.expand_prompt(message)
        command_result = await self.command_registry.dispatch(expanded)
        if command_result is not None:
            return self._persist_command_result(command_result)

        auto_compaction = self.compaction_service.maybe_auto_compact()
        if auto_compaction.applied:
            self._emit(AutoCompactionStart(reason=auto_compaction.reason or "threshold"))
            self._emit(
                AutoCompactionEnd(
                    result={"summary": auto_compaction.summary},
                    aborted=False,
                    willRetry=False,
                )
            )

        user_message = self.prompt_pipeline.build_user_message(expanded, images or [])
        context = self.session_manager.build_context().messages
        new_messages = await self.run_executor.run(prompts=[user_message], context=context)
        for msg in new_messages:
            self.session_manager.append_message(msg)
        return new_messages

    async def continue_run(self) -> list[AgentMessage]:
        context = self.session_manager.build_context().messages
        new_messages = await self.run_executor.run([], context)
        for msg in new_messages:
            self.session_manager.append_message(msg)
        return new_messages

    def _persist_command_result(self, result: CommandResult) -> list[AgentMessage]:
        if not result.persist:
            return []
        reply = AssistantMessage(content=[TextContent(text=result.message)], provider="system", model="gen")
        self.session_manager.append_message(reply)
        return [reply]
