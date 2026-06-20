# Lab 04 — Multi-Agent Orchestration

## What you'll learn
- Workflow pattern: deterministic pipelines with parallel steps
- Graph pattern: conditional routing to specialist agents
- MCP integration: markitdown (PDF→markdown) + duckduckgo (web search)
- Agents as tools: coordinator delegates to named specialists

## Files

| # | File | Pattern | MCP used |
|---|------|---------|----------|
| 01 | `01_blog_publisher.py` | Workflow | duckduckgo + markitdown |
| 02 | `02_resume_screener.py` | Workflow | markitdown (PDF parsing) |
| 03 | `03_code_reviewer.py` | Graph (routing) | — |
| 04 | `04_customer_triage.py` | Graph (routing) | — |

## Prerequisites

```bash
pip install mcp
# uv needed for MCP servers:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Run

```bash
python3 lab_04_multi_agent/01_blog_publisher.py
python3 lab_04_multi_agent/02_resume_screener.py
python3 lab_04_multi_agent/03_code_reviewer.py
python3 lab_04_multi_agent/04_customer_triage.py
```

## Key Takeaway

Different orchestration patterns for different problems:
- Workflow: fixed steps, order matters, some can run in parallel
- Graph: classify first, then route to the right specialist
- Both use agents-as-tools under the hood
