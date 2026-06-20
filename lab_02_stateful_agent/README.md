# Lab 02 — Stateful Agent

## What you'll learn
- `FileSessionManager` for persisting conversations locally
- `agent.state` for key-value data that survives restarts
- Custom tools that read/write state via `ToolContext`
- Multi-session isolation (one agent, many users)

## Files

| # | File | Use Case |
|---|------|----------|
| 01 | `01_basic_session.py` | Conversation persists across restarts |
| 02 | `02_personal_notes.py` | Add, search, list notes — survives quit |
| 03 | `03_todo_tracker.py` | Task management with status tracking |
| 04 | `04_user_preferences.py` | Agent learns and adapts to your style |
| 05 | `05_multi_session.py` | Multiple users, isolated state each |

## Run

```bash
python3 lab_02_stateful_agent/01_basic_session.py

# Multi-session: run as different users
python3 lab_02_stateful_agent/05_multi_session.py alice
python3 lab_02_stateful_agent/05_multi_session.py bob
```

## Key Takeaway

Same agent + `FileSessionManager` = conversations and state survive across restarts.
Sessions are just JSON files in `./sessions/` — inspect them to see how it works.
