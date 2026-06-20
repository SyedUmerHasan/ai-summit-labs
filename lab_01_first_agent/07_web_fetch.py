"""
Lab 01 — Your First Agent
07: Web Fetch + Save — agent that fetches web content and saves it locally
"""
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import http_request, file_write

SYSTEM_PROMPT = """You are a personal assistant that can fetch web pages and save them.
For normal chat, just respond. Only use tools when the user asks to fetch a URL or save something.
Respond in plain text, no markdown."""

agent = Agent(model=get_model(), tools=[http_request, file_write], system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler, interventions=[HumanInTheLoop(ask="stdio", allowed_tools=["http_request"])])


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Web Fetch Agent — Lab 01")
