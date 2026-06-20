# Lab 08 — Observability & Evals

## Problem
Take the Lab 05 helpdesk agent and **measure it**: trace every decision, capture metrics, test with adversarial inputs, and calculate a quality score.

## Concepts
- `AgentResult.metrics` and `traces`
- OpenTelemetry integration
- Hooks for lifecycle observability
- Evaluating tool selection accuracy
- Testing with edge cases and adversarial inputs

## Tasks (starter.py)
1. Add a hook that logs every tool call with timing
2. Run the agent on 5 test cases and collect metrics
3. Write an evaluator that scores tool selection correctness
4. Identify the failure modes

## Run
```bash
python starter.py
python solution.py
```
