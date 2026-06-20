"""
Lab 01 — Your First Agent
04: Read + Write — agent that reads a file, modifies it, writes it back
"""
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import file_read, file_write

SYSTEM_PROMPT = """You are a file editor with full read and write access.
You MUST use file_read to read and file_write to write. You CAN write files.
When editing: read first, make changes, write back. For normal chat, just respond.
Respond in plain text, no markdown."""

agent = Agent(model=get_model(), tools=[file_read, file_write], system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler, interventions=[HumanInTheLoop(ask="stdio", allowed_tools=["file_read"])])


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Read + Write Agent — Lab 01")
