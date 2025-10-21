from __future__ import annotations
from typing import Dict, List
from .agents.base import BaseAgent

class Router:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        # map kind -> agents that can handle it
        self.routes: Dict[str, List[BaseAgent]] = {}
        for a in agents:
            for k in a.supported_kinds():
                self.routes.setdefault(k, []).append(a)

    def for_kind(self, kind: str) -> List[BaseAgent]:
        return self.routes.get(kind, [])
