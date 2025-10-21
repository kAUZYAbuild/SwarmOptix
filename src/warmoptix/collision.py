from __future__ import annotations
from typing import List
from .types import Signal

def _tokenize(text: str) -> set[str]:
    return {t.lower() for t in (text or "").split() if t.strip()}

def jaccard(a: str, b: str) -> float:
    A, B = _tokenize(a), _tokenize(b)
    if not A and not B:
        return 1.0
    if not A or not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    return inter / union if union else 0.0

class CollisionDetector:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, signals: List[Signal]) -> List[Signal]:
        out: List[Signal] = []
        for s in signals:
            collided = False
            for t in out:
                if s.asset == t.asset and s.direction == t.direction:
                    if jaccard(s.explanation, t.explanation) >= self.similarity_threshold:
                        # keep the higher-confidence one
                        if s.confidence > t.confidence:
                            t.confidence = s.confidence
                            t.explanation = s.explanation
                        collided = True
                        break
            if not collided:
                out.append(s)
        return out
