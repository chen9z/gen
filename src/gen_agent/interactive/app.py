"""Minimal interactive REPL for gen-agent.

Async main loop with prompt_toolkit input and Rich output.
Slash commands delegate to session.prompt().
"""

from __future__ import annotations

import asyncio
import hashlib
import signal
import time
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from rich.console import Console
from rich.panel import Panel

from gen_agent.interactive.stream_view import StreamView


class InteractiveApp:
    """Minimal interactive REPL for gen-agent."""

    def __init__(self, session: Any, console: Console) -> None:
        self._session = session
        self._console = console
        self._prompt = self._build_prompt()
        self._active_task: asyncio.Task | None = None

    async def run(self, initial_message: str | None = None) -> int:
        """Main REPL loop."""
        self._print_welcome()
        if initial_message:
            await self._run_agent(initial_message)
        with patch_stdout(raw=True):
            while True:
                try:
                    text = await self._prompt.prompt_async()
                except (EOFError, KeyboardInterrupt):
                    break
                text = text.strip()
                if not text:
                    continue
                if text == "/quit":
                    break
                elif text == "/help":
                    self._print_help()
                else:
                    await self._run_agent(text)
        return 0

    async def _run_agent(self, prompt: str) -> None:
        """Run agent with streaming display and SIGINT handling."""
        view = StreamView(self._console)
        unsub = self._session.subscribe(view.on_event)
        view.start()

        loop = asyncio.get_running_loop()
        original_handler = signal.getsignal(signal.SIGINT)
        cancel_count = 0
        last_cancel = 0.0

        def _sigint_handler(sig: int, frame: Any) -> None:
            nonlocal cancel_count, last_cancel
            now = time.monotonic()
            if now - last_cancel < 1.5:
                cancel_count += 1
            else:
                cancel_count = 1
            last_cancel = now
            if cancel_count >= 2:
                signal.signal(signal.SIGINT, original_handler)
                raise KeyboardInterrupt
            if self._active_task and not self._active_task.done():
                loop.call_soon_threadsafe(self._active_task.cancel)

        try:
            signal.signal(signal.SIGINT, _sigint_handler)
            self._active_task = asyncio.create_task(
                self._session.prompt(prompt)
            )
            result = await self._active_task
            if result:
                for msg in (result if isinstance(result, list) else [result]):
                    text = _extract_text(msg)
                    if text:
                        self._console.print(text)
        except asyncio.CancelledError:
            self._console.print("[yellow]Interrupted.[/yellow]")
        except SystemExit:
            pass
        except Exception as exc:
            self._console.print(f"[red]Error: {exc}[/red]")
        finally:
            signal.signal(signal.SIGINT, original_handler)
            self._active_task = None
            view.stop()
            unsub()
            view.print_final(self._console)

    def _print_help(self) -> None:
        """Show common commands."""
        self._console.print(Panel(
            "Common commands:\n"
            "/quit     Exit the session\n"
            "/model    Switch model (e.g. /model gpt-4)\n"
            "/resume   Resume a session (e.g. /resume <id>)\n"
            "/compact  Trigger manual compaction\n"
            "/session  Show session info\n"
            "/help     Show this help\n"
            "\nShortcuts:\n"
            "Ctrl+C    Interrupt current agent run\n"
            "Ctrl+C\u00d72  Force quit\n"
            "\nAll /commands are handled by the session. "
            "Type any /command to see if it's available.",
            title="Help",
            border_style="cyan",
        ))

    def _print_welcome(self) -> None:
        """Show startup banner."""
        provider = getattr(self._session, "provider_name", "")
        model = getattr(self._session, "model_id", "default")
        display = f"{provider}/{model}" if provider else model
        self._console.print(Panel(
            f"Model: {display}",
            title="gen-agent",
            border_style="cyan",
        ))

    def _build_prompt(self) -> PromptSession:
        """Create prompt_toolkit session with minimal config."""
        commands = ["/quit", "/model", "/resume", "/help", "/compact", "/session"]
        return PromptSession(
            message="\u203a ",
            completer=WordCompleter(commands, sentence=True),
            history=FileHistory(str(self._history_path())),
        )

    def _history_path(self) -> Path:
        """History file per workspace, under config dir."""
        config_dir = Path.home() / ".config" / "gen-agent" / "user-history"
        config_dir.mkdir(parents=True, exist_ok=True)
        cwd_hash = hashlib.md5(str(Path.cwd()).encode()).hexdigest()[:12]
        return config_dir / f"{cwd_hash}.txt"


def _extract_text(message: Any) -> str:
    """Extract text from an assistant message.

    Content may be a string or a list of content blocks with .type/.text.
    """
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if getattr(block, "type", "") == "text":
                parts.append(getattr(block, "text", ""))
        return "\n".join(parts)
    return str(message)
