"""
Lab 04 — Multi-Agent Orchestration
04: Customer Triage — Graph pattern (conditional routing)

Pattern: Classifier routes customer messages to the right department.
"""
from strands import Agent
from strands.multiagent import GraphBuilder
from shared.model_config import get_model

classifier = Agent(
    model=get_model(),
    name="classifier",
    system_prompt="You classify customer support messages. Respond with ONLY one word: BILLING, TECHNICAL, SALES, or ESCALATION. Nothing else.",
    callback_handler=None,
)

billing_agent = Agent(
    model=get_model(),
    name="billing_agent",
    system_prompt="You are a billing specialist. Handle refund requests, invoice questions, payment issues, subscription changes. Be empathetic, provide clear steps. Plain text, no markdown.",
)

tech_support = Agent(
    model=get_model(),
    name="tech_support",
    system_prompt="You are technical support. Troubleshoot bugs, connectivity, API errors, integration problems. Ask clarifying questions, provide step-by-step solutions. Plain text, no markdown.",
)

sales_agent = Agent(
    model=get_model(),
    name="sales_agent",
    system_prompt="You are a sales specialist. Handle upgrade requests, pricing questions, feature comparisons, enterprise inquiries. Be helpful, provide clear options. Plain text, no markdown.",
)

escalation_agent = Agent(
    model=get_model(),
    name="escalation_agent",
    system_prompt="You are a senior escalation manager. Handle cases others could not resolve, or angry customers. Apologize sincerely, offer concrete resolutions, provide compensation if appropriate. Plain text, no markdown.",
)


def is_billing(state):
    result = state.results.get("classifier")
    if not result:
        return False
    return "BILLING" in str(result.result).upper()


def is_technical(state):
    result = state.results.get("classifier")
    if not result:
        return False
    return "TECHNICAL" in str(result.result).upper()


def is_sales(state):
    result = state.results.get("classifier")
    if not result:
        return False
    return "SALES" in str(result.result).upper()


def is_escalation(state):
    result = state.results.get("classifier")
    if not result:
        return False
    return "ESCALATION" in str(result.result).upper()


builder = GraphBuilder()

builder.add_node(classifier, "classifier")
builder.add_node(billing_agent, "billing_agent")
builder.add_node(tech_support, "tech_support")
builder.add_node(sales_agent, "sales_agent")
builder.add_node(escalation_agent, "escalation_agent")

builder.add_edge("classifier", "billing_agent", condition=is_billing)
builder.add_edge("classifier", "tech_support", condition=is_technical)
builder.add_edge("classifier", "sales_agent", condition=is_sales)
builder.add_edge("classifier", "escalation_agent", condition=is_escalation)

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
    run_chat(graph, title="Customer Triage (Graph) — Lab 04")
