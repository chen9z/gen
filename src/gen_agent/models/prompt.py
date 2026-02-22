from __future__ import annotations

from dataclasses import dataclass, field

from .content import ImageContent


@dataclass(slots=True)
class PromptInput:
    text: str
    images: list[ImageContent] = field(default_factory=list)
