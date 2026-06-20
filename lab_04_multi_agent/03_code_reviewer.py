"""
Lab 04 — Multi-Agent Orchestration
03: Code Reviewer — Graph pattern (conditional routing)

Pattern: GraphBuilder with nodes, edges, and conditional routing.
Classifier routes to the right specialist based on code type.
"""
import os
from strands import Agent
from strands.multiagent import GraphBuilder
from strands_tools import file_read
from shared.model_config import get_model

# Specialized agents
classifier = Agent(
    model=get_model(),
    name="classifier",
    tools=[file_read],
    system_prompt="You classify code for review. If given a file path, read it first. Then respond with ONLY one word: SECURITY, PERFORMANCE, or STYLE. Nothing else.",
    callback_handler=None,
)

security_reviewer = Agent(
    model=get_model(),
    name="security_reviewer",
    tools=[file_read],
    system_prompt="You are a security code reviewer. If given a file path, read it. Analyze for: SQL injection, XSS, auth flaws, exposed secrets. List findings with severity. Plain text, no markdown.",
)

performance_reviewer = Agent(
    model=get_model(),
    name="performance_reviewer",
    tools=[file_read],
    system_prompt="You are a performance code reviewer. If given a file path, read it. Analyze for: N+1 queries, unnecessary loops, memory leaks, missing caching. Plain text, no markdown.",
)

style_reviewer = Agent(
    model=get_model(),
    name="style_reviewer",
    tools=[file_read],
    system_prompt="You are a style code reviewer. If given a file path, read it. Check: naming conventions, function length, duplication, readability, error handling. Plain text, no markdown.",
)


# Conditional edge functions
def is_security(state):
    result = state.results.get("classifier")
    if not result:
        return False
    text = str(result.result).upper()
    return "SECURITY" in text


def is_performance(state):
    result = state.results.get("classifier")
    if not result:
        return False
    text = str(result.result).upper()
    return "PERFORMANCE" in text


def is_style(state):
    result = state.results.get("classifier")
    if not result:
        return False
    text = str(result.result).upper()
    return "STYLE" in text


# Build the graph
builder = GraphBuilder()

builder.add_node(classifier, "classifier")
builder.add_node(security_reviewer, "security_reviewer")
builder.add_node(performance_reviewer, "performance_reviewer")
builder.add_node(style_reviewer, "style_reviewer")

builder.add_edge("classifier", "security_reviewer", condition=is_security)
builder.add_edge("classifier", "performance_reviewer", condition=is_performance)
builder.add_edge("classifier", "style_reviewer", condition=is_style)

builder.set_entry_point("classifier")
builder.set_execution_timeout(120)

graph = builder.build()


from shared.terminal import run_chat


def invoke(message: str, history: list = None):
    result = graph(message)
    print(f"\n  Status: {result.status}")
    print(f"  Route: {' -> '.join(n.node_id for n in result.execution_order)}")
    return result


if __name__ == "__main__":
    run_chat(graph, title="Code Reviewer (Graph) — Lab 04")
