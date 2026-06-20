# Lab 01 — Your First Agent

## What you'll learn
- What an Agent is: model + system prompt (no tools)
- Adding tools one at a time to give the agent capabilities
- Human-in-the-loop approval for destructive actions
- Progressive complexity: read → write → create → web

## Files (run in order)

| # | File | Concept | Tools |
|---|------|---------|-------|
| 01 | `01_basic_agent.py` | Agent with no tools — just talks | None |
| 02 | `02_read_file.py` | Agent that reads files | `file_read` |
| 03 | `03_write_file.py` | Agent that writes files (with approval) | `file_write` |
| 04 | `04_read_write_file.py` | Agent that reads + modifies + saves | `file_read`, `file_write` |
| 05 | `05_create_file.py` | Agent that creates new files from description | `file_write`, `shell` |
| 06 | `06_web_search.py` | Agent that fetches web pages | `http_request` |
| 07 | `07_web_fetch.py` | Agent that fetches + saves locally | `http_request`, `file_write` |

## Run

```bash
cd ai-summit-labs
PYTHONPATH=. python lab_01_first_agent/01_basic_agent.py
PYTHONPATH=. python lab_01_first_agent/02_read_file.py
# ... etc
```

## Key Takeaway

Same `Agent` class — add tools to give it new powers, add interventions to keep humans in control.
