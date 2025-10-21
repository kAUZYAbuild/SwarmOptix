from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager

class AsyncSemaphorePool:
    """Holds semaphores keyed by name so we can adjust concurrency on the fly."""
    def __init__(self):
        self._locks: dict[str, asyncio.Semaphore] = {}

    def get(self, key: str, value: int):
        sem = self._locks.get(key)
        # Recreate if size changed
        if sem is None or getattr(sem, "_value", None) != value:
            sem = asyncio.Semaphore(value)
            self._locks[key] = sem
        return sem

@asynccontextmanager
async def acquire(sem: asyncio.Semaphore):
    await sem.acquire()
    try:
        yield
    finally:
        sem.release()
