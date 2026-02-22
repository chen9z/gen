from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path

from gen_agent.models.content import TextContent
from gen_agent.models.tools import BashInput

from .base import Tool
from .truncate import DEFAULT_MAX_BYTES, format_size, truncate_tail


class BashTool(Tool):
    name = "bash"
    label = "bash"
    description = "Execute shell command in cwd. Returns stdout+stderr with tail truncation."
    input_model = BashInput

    def __init__(self, cwd: str, command_prefix: str | None = None):
        self.cwd = cwd
        self.command_prefix = command_prefix

    async def execute(self, params: BashInput) -> tuple[list[TextContent], dict | None]:
        command = params.command
        if self.command_prefix:
            command = f"{self.command_prefix}\n{command}"

        proc = await asyncio.create_subprocess_shell(
            command,
            cwd=self.cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            executable=os.environ.get("SHELL", "/bin/zsh"),
        )

        try:
            raw, _ = await asyncio.wait_for(proc.communicate(), timeout=params.timeout)
        except asyncio.TimeoutError:
            proc.kill()
            timeout_raw, _ = await proc.communicate()
            timeout_output = (timeout_raw or b"").decode("utf-8", errors="replace")
            timeout_trunc = truncate_tail(timeout_output)
            timeout_text = timeout_trunc["content"] or ""
            if timeout_text:
                timeout_text += "\n\n"
            timeout_text += f"Command timed out after {params.timeout} seconds"
            raise TimeoutError(timeout_text)

        output = (raw or b"").decode("utf-8", errors="replace")
        trunc = truncate_tail(output)
        text = trunc["content"] or "(no output)"

        details = None
        if trunc["truncated"]:
            fd, full_path = tempfile.mkstemp(prefix="gen-bash-", suffix=".log")
            os.close(fd)
            Path(full_path).write_text(output, encoding="utf-8")
            text += f"\n\n[Output truncated at {format_size(DEFAULT_MAX_BYTES)}. Full output: {full_path}]"
            details = {"truncation": trunc, "fullOutputPath": full_path}

        if proc.returncode and proc.returncode != 0:
            raise RuntimeError(f"{text}\n\nCommand exited with code {proc.returncode}")

        return [TextContent(text=text)], details
