from __future__ import annotations
import asyncio
import typer
from pathlib import Path
from .orchestrator import Orchestrator
from .types import Task

app = typer.Typer(add_completion=False, no_args_is_help=True)

@app.command()
def demo(file: Path = typer.Option(..., exists=True, help="Text file; each line is a blurb"),
         asset: str = typer.Option("DEMO", help="Asset symbol to tag signals with")):
    """Run a simple sentiment→execution pipeline over a file of lines."""
    orch = Orchestrator()

    async def _run():
        lines = [ln.strip() for ln in file.read_text(encoding="utf-8").splitlines() if ln.strip()]
        for ln in lines:
            t = Task(kind="text.sentiment", payload={"text": ln}, metadata={"asset": asset})
            dedup = await orch.submit(t)
            typer.echo(f"INPUT: {ln}")
            for s in dedup:
                typer.echo(f"  → {s.asset} {s.direction} conf={s.confidence:.2f} src={s.source}")
        typer.echo("\nLedger:")
        for fill in orch.status()["ledger"]:
            typer.echo(f"  {fill}")

    asyncio.run(_run())

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Run the FastAPI server."""
    import uvicorn
    uvicorn.run("warmoptix.server:app", host=host, port=port, reload=False)

@app.command()
def status():
    orch = Orchestrator()
    typer.echo(orch.status())

def main():
    app()
