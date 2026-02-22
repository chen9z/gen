from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from gen_agent.models.content import UserContentBlock


class Tool:
    name: str
    label: str
    description: str
    input_model: type[BaseModel]

    async def execute(self, params: BaseModel) -> tuple[list[UserContentBlock], Any | None]:
        raise NotImplementedError
