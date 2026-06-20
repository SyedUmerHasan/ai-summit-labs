# AI Summit Labs — Strands Agents

Progressive hands-on labs from a single agent to multi-agent orchestration with observability.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
docker exec ollama ollama pull llama3.1
```

### 2. Set up Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # bash/zsh
source .venv/bin/activate.fish   # fish
pip install -e .
pip install -r requirements.txt
```

### 3. Run a lab

```bash
python3 lab_01_first_agent/01_basic_agent.py
```

## Labs

| Lab | Pattern | Files |
|-----|---------|-------|
| 01 | Single Agent + Tools | basic, read, write, create, web search, web fetch |
| 02 | State + Sessions | sessions, notes, todos, preferences, multi-user, full agent |
| 03 | Agents as Tools | tech planner, user stories, sprint, proposal, meeting, incident, email, coding assistant |
| 04 | Multi-Agent Orchestration | sequential workflow, resume screener, graph (code review, triage), swarm (call center) |
| 05 | Observability | Langfuse tracing (auto-enabled for all labs) |

## Model Config

All labs use `shared/model_config.py`. Switch models via env var:

```bash
# Default: Anthropic Claude
python3 lab_01_first_agent/01_basic_agent.py

# Ollama local
MODEL=ollama python3 lab_01_first_agent/01_basic_agent.py

# AWS Bedrock
MODEL=bedrock python3 lab_01_first_agent/01_basic_agent.py
```

## Infrastructure

| Service | Port | Purpose |
|---------|------|---------|
| Ollama | 11434 | Local LLM |
| Langfuse | 3000 | Observability dashboard |

## Observability

All labs auto-trace to Langfuse when keys are set:

```bash
set -Ux LANGFUSE_PUBLIC_KEY "pk-lf-..."
set -Ux LANGFUSE_SECRET_KEY "sk-lf-..."
set -Ux LANGFUSE_BASE_URL "http://localhost:3000"
```

View traces at http://localhost:3000
