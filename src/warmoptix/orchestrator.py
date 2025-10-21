from __future__ import annotations
import asyncio
from typing import List
from .types import Task, Signal
from .router import Router
from .budget import BudgetManager
from .collision import CollisionDetector
from .utils import AsyncSemaphorePool, acquire
from .agents.sentiment import SentimentAgent
from .agents.execution import ExecutionAgent

class Orchestrator:
    def __init__(self):
        self.budgets = BudgetManager()
        self.collision = CollisionDetector()
        # default agents
        self.sentiment = SentimentAgent()
        self.execution = ExecutionAgent()
        self.agents = [self.sentiment, self.execution]
        self.router = Router(self.agents)
        self.pool = AsyncSemaphorePool()

    async def _run_agent(self, agent, task: Task) -> List[Signal] | None:
        # Adjust concurrency for this agent from budget
        c = self.budgets.update_concurrency(agent.name)
        sem = self.pool.get(agent.name, c)
        async with acquire(sem):
            self.budgets.consume(agent.name, amount=1)
            try:
                return await agent.handle(task)
            finally:
                # light refill to avoid starvation; in a real system tie to wall time or tokens
                self.budgets.refill(agent.name, amount=1)

    async def submit(self, task: Task):
        # Stage 1: route text.sentiment → SentimentAgent(s)
        agents = self.router.for_kind(task.kind)
        if not agents:
            return []
        stage1 = await asyncio.gather(*[self._run_agent(a, task) for a in agents])
        signals = [s for out in stage1 if out for s in out]
        if not signals:
            return []
        # Collision detection
        dedup = self.collision.deduplicate(signals)
        # Stage 2: wrap into execution task
        exec_task = Task(kind="signal.execute", payload={"signals": dedup}, metadata={})
        await self._run_agent(self.execution, exec_task)
        return dedup

    def status(self):
        return {
            "budgets": self.budgets.snapshot(),
            "ledger": self.execution.snapshot(),
        }
