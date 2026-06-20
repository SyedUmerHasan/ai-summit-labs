"""
Lab 01 — Your First Agent
05: Create File — agent that generates new files from a description
"""
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import file_write, shell

SYSTEM_PROMPT = """You are a file creator. You generate files from descriptions.
Use shell to create directories if needed. Use file_write to create files.
For normal chat, just respond. Respond in plain text, no markdown."""

agent = Agent(model=get_model(), tools=[file_write, shell], system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler, interventions=[HumanInTheLoop(ask="stdio")])


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Create File Agent — Lab 01")
