# Lab 03 — Agents as Tools

## What you'll learn
- One agent calling other agents as tools (delegation)
- Specialist sub-agents with focused system prompts
- Coordinator pattern: orchestrate a team of AI specialists
- Building toward a Claude Code-like system

## Files

| # | File | Use Case | Sub-agents |
|---|------|----------|-----------|
| 01 | `01_tech_planner.py` | Plan a feature implementation | Architect, Task Planner, Estimator |
| 02 | `02_user_stories.py` | Generate user stories from idea | Feature Analyst, Story Writer, Criteria Checker |
| 03 | `03_sprint_planner.py` | Distribute work for a quarter | Capacity Planner, Distributor, Timeline Builder |
| 04 | `04_proposal_writer.py` | Write a business proposal | Researcher, Writer, Reviewer |
| 05 | `05_meeting_prep.py` | Prepare meeting agenda | Context Analyzer, Agenda Builder, Action Tracker |
| 06 | `06_incident_report.py` | Write a post-mortem | Timeline Builder, Root Cause Analyzer, Report Writer |
| 07 | `07_email_writer.py` | Draft professional emails | Tone Analyzer, Drafter, Polisher |
| 08 | `08_coding_assistant.py` | Full coding CLI (Claude Code-like) | All tools: think, read, write, edit, shell, http |

## Run

```bash
python3 lab_03_agents_as_tools/01_tech_planner.py
python3 lab_03_agents_as_tools/08_coding_assistant.py
```

## Key Takeaway

Pass agents directly as tools: `tools=[agent_a, agent_b]`. The SDK auto-wraps them.
The coordinator decides who to call based on the task. Same pattern, different specialists.
