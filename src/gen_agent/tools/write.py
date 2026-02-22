from __future__ import annotations

from gen_agent.models.content import TextContent
from gen_agent.models.tools import WriteInput

from .base import Tool
from .path_utils import resolve_to_cwd


class WriteTool(Tool):
    name = "write"
    label = "write"
    description = "Write content to a file. Creates parent directories and overwrites existing files."
    input_model = WriteInput

    def __init__(self, cwd: str):
        self.cwd = cwd

    async def execute(self, params: WriteInput) -> tuple[list[TextContent], None]:
        path = resolve_to_cwd(params.path, self.cwd)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(params.content, encoding="utf-8")
        written_bytes = len(params.content.encode("utf-8"))
        return [TextContent(text=f"Successfully wrote {written_bytes} bytes to {params.path}")], None
