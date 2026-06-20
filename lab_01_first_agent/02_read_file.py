"""
Lab 01 — Your First Agent
02: Read File — agent that can read any file on your machine
"""
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat
from strands_tools import file_read

SYSTEM_PROMPT = """You are a personal assistant that can read files.
For normal chat, just respond. Only use file_read when the user asks to read a specific file.
Respond in plain text, no markdown."""

agent = Agent(model=get_model(), tools=[file_read], system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Read File Agent — Lab 01")
