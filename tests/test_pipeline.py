from warmoptix.orchestrator import Orchestrator
from warmoptix.types import Task
import asyncio

async def _run():
    orch = Orchestrator()
    t1 = Task(kind="text.sentiment", payload={"text": "love strong green"}, metadata={"asset":"DEMO"})
    t2 = Task(kind="text.sentiment", payload={"text": "love strong green"}, metadata={"asset":"DEMO"})
    s1 = await orch.submit(t1)
    s2 = await orch.submit(t2)
    # ensure signals produced and system stays healthy
    assert len(s1) >= 1
    assert len(s2) >= 1
    st = orch.status()
    assert "budgets" in st and "ledger" in st

def test_pipeline():
    asyncio.run(_run())
