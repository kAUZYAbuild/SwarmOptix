from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from .orchestrator import Orchestrator
from .types import Task

app = FastAPI(title="warmOptix API")
ORCH = Orchestrator()

class TaskIn(BaseModel):
    kind: str
    payload: dict
    metadata: dict | None = None

@app.get("/")
def root():
    return {"name": "warmOptix", "endpoints": ["/submit", "/status"]}

@app.post("/submit")
async def submit(task: TaskIn):
    t = Task(kind=task.kind, payload=task.payload, metadata=task.metadata or {})
    sigs = await ORCH.submit(t)
    return {"signals": [vars(s) for s in sigs], "status": ORCH.status()}

@app.get("/status")
def status():
    return ORCH.status()
