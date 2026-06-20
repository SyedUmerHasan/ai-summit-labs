# Lab 05 — Observability

## What you'll learn
- Auto-tracing with Langfuse + OpenTelemetry
- Every agent call, tool use, and model request captured automatically
- View traces, latency, token usage in the Langfuse dashboard

## Prerequisites

```bash
docker compose up -d   # starts Langfuse at http://localhost:3000
pip install 'strands-agents[otel]' langfuse
```

Set your Langfuse keys (from http://localhost:3000 project settings):
```bash
set -Ux LANGFUSE_PUBLIC_KEY "pk-lf-..."
set -Ux LANGFUSE_SECRET_KEY "sk-lf-..."
set -Ux LANGFUSE_BASE_URL "http://localhost:3000"
```

## Files

| # | File | What it shows |
|---|------|--------------|
| 01 | `01_langfuse_basic.py` | Basic tracing — run agent, see traces in dashboard |

## Key Takeaway

Zero code changes needed. Langfuse auto-captures all Strands OTEL spans.
All other labs (01-04) also trace automatically via `shared/__init__.py`.
