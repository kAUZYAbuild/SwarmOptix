from __future__ import annotations
from .types import Budget

class BudgetManager:
    def __init__(self):
        # default budgets by agent name
        self._budgets: dict[str, Budget] = {}

    def ensure(self, agent_name: str) -> Budget:
        if agent_name not in self._budgets:
            self._budgets[agent_name] = Budget(name=agent_name)
        return self._budgets[agent_name]

    def update_concurrency(self, agent_name: str) -> int:
        b = self.ensure(agent_name)
        # Simple rule: scale with remaining_quanta
        # e.g., every 50 quanta adds 1 concurrency up to cap
        scaled = b.min_concurrency + min(b.max_concurrency_cap - b.min_concurrency, b.remaining_quanta // 50)
        b.max_concurrency = max(b.min_concurrency, min(scaled, b.max_concurrency_cap))
        return b.max_concurrency

    def consume(self, agent_name: str, amount: int = 1):
        b = self.ensure(agent_name)
        b.remaining_quanta = max(0, b.remaining_quanta - amount)
        self.update_concurrency(agent_name)

    def refill(self, agent_name: str, amount: int = 25):
        b = self.ensure(agent_name)
        b.remaining_quanta = min(400, b.remaining_quanta + amount)
        self.update_concurrency(agent_name)

    def snapshot(self):
        return {k: vars(v) for k, v in self._budgets.items()}
