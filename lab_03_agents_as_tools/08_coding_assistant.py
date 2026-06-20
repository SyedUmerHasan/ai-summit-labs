"""
Lab 03 — Agents as Tools
08: Coding Assistant — a Claude Code-like CLI agent
"""
import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import think, file_read, file_write, editor, shell, http_request
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="coding-assistant",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = """You are an expert coding assistant running in the user's terminal.

Capabilities:
- think: plan your approach before complex tasks
- file_read: read any file
- file_write: create new files
- editor: make targeted edits to existing files
- shell: run any shell command (git, tests, build, ls, grep, etc.)
- http_request: fetch documentation or API references online

Workflow:
1. When given a project, scan it first (shell: ls or find, limit depth)
2. Read relevant files to understand the codebase
3. Plan with think if the task is complex
4. Make changes with editor or file_write
5. Run tests or build to verify
6. Summarize what you did

Rules:
- Always understand before changing. Read first, edit second.
- Do NOT scan recursively into node_modules, .venv, or __pycache__
- Keep shell commands short and focused
- For normal conversation, just respond. No tools needed.
- Never fabricate data.
- Plain text output, no markdown formatting."""

agent = Agent(
    model=get_model(),
    tools=[think, file_read, file_write, editor, shell, http_request],
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
    interventions=[HumanInTheLoop(ask="stdio", allowed_tools=["think", "file_read", "http_request"])],
)


def invoke(message: str, history: list = None):
    return agent(message, limits={"turns": 15})


if __name__ == "__main__":
    run_chat(agent, title="Coding Assistant — Lab 03")
