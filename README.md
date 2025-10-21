# warmOptix

**Modular swarm optimizer** for multi-agent systems. It load-balances work across agents (e.g., one for sentiment, one for execution), detects **collisions** (redundant/overlapping signals), and **auto-scales** concurrency based on compute budgets. Ships with a CLI demo and a FastAPI server so people can actually use it.

## Features
- Async **load-balancing** router per agent
- **Collision detection** for redundant signals (token Jaccard + windowed coalescing)
- **Auto-scaling** concurrency per agent from compute budgets
- Pluggable **Agents** (Sentiment, Execution) with a simple Base API

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip && pip install -e .

warmoptix demo --file examples/tweets.txt --asset DEMO

warmoptix serve --host 0.0.0.0 --port 8000
# Submit a task:
curl -X POST http://localhost:8000/submit \
  -H 'Content-Type: application/json' \
  -d '{"kind":"text.sentiment","payload":{"text":"Bulls in control"},"metadata":{"asset":"BTC"}}'
