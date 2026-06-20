"""
Lab 01 — Your First Agent
01: Basic Agent — no tools, just a model + prompt
"""
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SYSTEM_PROMPT = """You are a helpful assistant. Respond in plain text, no markdown."""

agent = Agent(model=get_model(), system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Basic Agent — Lab 01")
