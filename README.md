# AI Summit Labs — Strands Agents

Progressive hands-on labs from a single agent to self-healing, self-learning AI systems.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose

## Quick Start

### 1. Start Ollama

```bash
docker compose up -d
docker exec ollama ollama pull qwen2.5:3b
```

### 2. Set up Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run a lab

```bash
PYTHONPATH=. python lab_01_first_agent/solution.py
```

## Labs

| Lab | Pattern | Problem |
|-----|---------|---------|
| 01 | Single Agent + Tools | Research assistant |
| 02 | State + Memory | Customer support bot |
| 03 | Agents as Tools | Document review pipeline |
| 04 | Workflow (SOP) | Employee onboarding DAG |
| 05 | Graph (Routing) | IT helpdesk ticket router |
| 06 | Swarm | Incident response team |
| 07 | Agent-to-Agent (A2A) | Cross-team code review |
| 08 | Observability & Evals | Measure and test agents |
| 09 | Self-Healing | DevOps monitor + auto-recover |
| 10 | Self-Learning | Memory extraction + improvement loop |

## Model Config

All labs use `shared/model_config.py`. Override the model via env var:

```bash
# Default: Ollama qwen2.5:3b
PYTHONPATH=. python lab_01_first_agent/solution.py

# Use Bedrock instead
MODEL_PROVIDER=bedrock PYTHONPATH=. python lab_01_first_agent/solution.py
```
