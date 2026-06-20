"""
Lab 02 — Stateful Agent
01: Basic Session — agent remembers conversation across restarts
Run this, chat, quit, run again — it remembers everything.
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="basic-session",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = """You are a personal assistant with persistent memory.
You remember everything from previous conversations.
When the user returns, greet them and reference what you discussed before.
Respond in plain text, no markdown."""

agent = Agent(
    model=get_model(),
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Basic Session — Lab 02")
