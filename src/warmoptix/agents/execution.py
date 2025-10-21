from __future__ import annotations
from typing import List
from ..types import Task, Signal
from .base import BaseAgent

class ExecutionAgent(BaseAgent):
    name = "execution"

    def __init__(self):
        self.ledger: list[dict] = []  # simulated fills

    def supported_kinds(self) -> List[str]:
        # This agent consumes signals wrapped as tasks
        return ["signal.execute"]

    async def handle(self, task: Task) -> List[Signal] | None:
        signals: List[Signal] = task.payload.get("signals", [])
        for s in signals:
            side = "BUY" if s.direction == "bullish" else ("SELL" if s.direction == "bearish" else "HOLD")
            fill = {
                "asset": s.asset,
                "side": side,
                "qty": round(1.0 * s.confidence, 3),
                "confidence": s.confidence,
                "source": s.source,
                "explanation": s.explanation,
            }
            self.ledger.append(fill)
        return None  # no downstream signals

    def snapshot(self):
        return list(self.ledger)
