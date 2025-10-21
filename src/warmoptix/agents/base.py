from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from ..types import Task, Signal

class BaseAgent(ABC):
    name: str = "agent"

    @abstractmethod
    def supported_kinds(self) -> List[str]:
        ...

    @abstractmethod
    async def handle(self, task: Task) -> List[Signal] | None:
        ...
