"""
Lab 04 — Multi-Agent Orchestration
05: Call Center Swarm — agents collaborate autonomously to resolve customer issues

Pattern: Swarm — agents hand off to each other based on what they discover.
Unlike Graph (fixed routing), the path emerges from the conversation.
"""
from strands import Agent
from strands.multiagent import Swarm
from shared.model_config import get_model

greeter = Agent(
    model=get_model(),
    name="greeter",
    description="First point of contact. Greets customer, understands their issue, hands off to the right specialist.",
    system_prompt="""You are the first point of contact at a call center. 
Greet the customer warmly, understand their issue, then hand off to the right specialist:
- billing_specialist: for payment, charges, refunds, invoices
- tech_support: for errors, bugs, connectivity, app not working
- account_manager: for account changes, upgrades, cancellations
- escalation_manager: for angry customers or complex unresolved issues
Always hand off — never try to resolve issues yourself. Plain text, no markdown.""",
)

billing_specialist = Agent(
    model=get_model(),
    name="billing_specialist",
    description="Handles payment disputes, refunds, invoice questions, and charge explanations.",
    system_prompt="""You are a billing specialist at a call center.
Handle: refunds, payment disputes, invoice questions, charge explanations, payment plan setup.
If the customer is angry or the issue is beyond your authority, hand off to escalation_manager.
If the issue turns out to be technical, hand off to tech_support.
If resolved, thank the customer and end the conversation. Plain text, no markdown.""",
)

tech_support = Agent(
    model=get_model(),
    name="tech_support",
    description="Troubleshoots technical issues: app errors, login problems, connectivity, bugs.",
    system_prompt="""You are technical support at a call center.
Handle: app crashes, login issues, error messages, connectivity problems, slow performance.
Walk through troubleshooting steps. If the issue requires an account change, hand off to account_manager.
If the customer is frustrated and wants to escalate, hand off to escalation_manager.
If resolved, confirm the fix and end the conversation. Plain text, no markdown.""",
)

account_manager = Agent(
    model=get_model(),
    name="account_manager",
    description="Handles account changes: upgrades, downgrades, cancellations, profile updates.",
    system_prompt="""You are an account manager at a call center.
Handle: plan upgrades/downgrades, cancellation requests, profile updates, feature access.
If cancelling, try to retain with offers. If billing questions arise, hand off to billing_specialist.
If resolved, confirm changes and end the conversation. Plain text, no markdown.""",
)

escalation_manager = Agent(
    model=get_model(),
    name="escalation_manager",
    description="Senior manager for angry customers and unresolved complex issues.",
    system_prompt="""You are a senior escalation manager at a call center.
Handle: angry customers, unresolved issues, compensation requests, complaints about service.
Apologize sincerely, take ownership, offer concrete resolution (refund, credit, free months).
You are the final stop — do NOT hand off to anyone else. Resolve it here.
Plain text, no markdown.""",
)

swarm = Swarm(
    [greeter, billing_specialist, tech_support, account_manager, escalation_manager],
    entry_point=greeter,
    max_handoffs=6,
    max_iterations=10,
    execution_timeout=300.0,
    node_timeout=120.0,
)


from shared.terminal import run_chat


def invoke(message: str, history: list = None):
    result = swarm(message)
    print(f"\n  Status: {result.status}")
    print(f"  Agent path: {' -> '.join(n.node_id for n in result.node_history)}")
    return result


if __name__ == "__main__":
    run_chat(swarm, title="Call Center Swarm — Lab 04")
