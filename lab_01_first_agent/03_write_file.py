"""
Lab 01 — Your First Agent
03: Write File — agent that can write content to files
"""
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import file_write

SYSTEM_PROMPT = """You are a personal assistant that can write files.
For normal chat, just respond. Only use file_write when the user asks to create or write a file.
Respond in plain text, no markdown."""

agent = Agent(model=get_model(), tools=[file_write], system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler, interventions=[HumanInTheLoop(ask="stdio")])


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Write File Agent — Lab 01")
