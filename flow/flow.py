from dataclasses import dataclass
from typing import Optional, Any, List


@dataclass
class NextTask:
    id: str
    inputs: Optional[dict[str, Any]] = None
    spawn_another: bool = False


@dataclass
class TaskOutput:
    output: Any
    next_task: Optional[List[NextTask]] = None


