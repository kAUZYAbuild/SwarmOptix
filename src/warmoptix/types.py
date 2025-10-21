from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time

@dataclass
class Task:
    kind: str  # e.g., "text.sentiment"
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: time.time())

@dataclass
class Signal:
    asset: str
    direction: str  # "bullish" | "bearish" | "neutral"
    confidence: float
    source: str  # agent name
    explanation: str = ""
    ts: float = field(default_factory=lambda: time.time())

@dataclass
class Result:
    ok: bool
    data: Any = None
    error: Optional[str] = None

@dataclass
class Budget:
    name: str
    max_concurrency: int = 1
    remaining_quanta: int = 100  # abstract compute units
    min_concurrency: int = 1
    max_concurrency_cap: int = 8
