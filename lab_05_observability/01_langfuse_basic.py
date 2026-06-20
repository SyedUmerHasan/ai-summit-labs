"""
Lab 05 — Observability
01: Langfuse Basic — auto-trace every agent call to Langfuse

Just run this file — traces appear at http://localhost:3000 within seconds.
Strands auto-emits OpenTelemetry spans. Langfuse captures them automatically.
"""
from langfuse import get_client
from strands import Agent
from strands_tools import calculator, current_time
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

# Initialize Langfuse — this sets up OTEL TracerProvider automatically
langfuse = get_client()

if langfuse.auth_check():
    print("  Langfuse connected: http://localhost:3000")
else:
    print("  WARNING: Langfuse auth failed. Check your keys.")

agent = Agent(
    model=get_model(),
    tools=[calculator, current_time],
    system_prompt="You are a helpful assistant. You can do math and check the time. Plain text, no markdown.",
    callback_handler=callback_handler,
)


def invoke(message: str, history: list = None):
    result = agent(message)
    langfuse.flush()
    return result


if __name__ == "__main__":
    run_chat(agent, title="Langfuse Tracing — Lab 05")
    langfuse.flush()
