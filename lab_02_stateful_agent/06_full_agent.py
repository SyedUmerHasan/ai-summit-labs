"""
Lab 02 — Stateful Agent
06: Full Agent — search, fetch, read, write, think + persistent session
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import http_request, file_read, file_write, think
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="full-agent-session",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = """You are a powerful personal assistant with persistent memory and full capabilities:
- Think: reason through complex problems before acting
- Read: read any file on the local machine
- Write: create or update files
- Fetch: fetch web pages or call APIs

You remember all previous conversations. When the user returns, reference past context.
Rules:
- For normal chat, just respond — no tools needed
- Only use tools when the user asks for something that requires them
- Use think for complex multi-step tasks before diving in
- Never fabricate data — only report what tools actually return
Respond in plain text, no markdown."""

agent = Agent(
    model=get_model(),
    tools=[think, http_request, file_read, file_write],
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
    interventions=[HumanInTheLoop(ask="stdio", allowed_tools=["think", "file_read", "http_request"])],
)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Full Agent — Lab 02")
