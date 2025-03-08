from dataclasses import dataclass


@dataclass
class Document:
    title: str
    content: str
    start_line: int
    end_line: int
    metadata: dict
