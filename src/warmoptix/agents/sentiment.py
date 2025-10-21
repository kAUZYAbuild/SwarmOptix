from __future__ import annotations
from typing import List
from ..types import Task, Signal
from .base import BaseAgent

_POS = {
    "love","great","good","bull","moon","pump","win","profit","green","up","soar","strong","buy"
}
_NEG = {
    "hate","bad","bear","dump","lose","loss","red","down","crash","weak","sell"
}

class SentimentAgent(BaseAgent):
    name = "sentiment"

    def supported_kinds(self) -> List[str]:
        return ["text.sentiment"]

    async def handle(self, task: Task) -> List[Signal] | None:
        text = (task.payload or {}).get("text", "")
        asset = (task.metadata or {}).get("asset", "DEMO")
        tokens = [t.lower() for t in text.split()]
        pos = sum(1 for t in tokens if t in _POS)
        neg = sum(1 for t in tokens if t in _NEG)
        if pos == 0 and neg == 0:
            direction = "neutral"
            conf = 0.5
        else:
            score = pos - neg
            direction = "bullish" if score > 0 else ("bearish" if score < 0 else "neutral")
            conf = min(0.99, max(0.51, abs(score) / max(1, len(tokens))))
        sig = Signal(asset=asset, direction=direction, confidence=conf, source=self.name,
                     explanation=f"pos={pos}, neg={neg}, text='{text[:120]}'")
        return [sig]
