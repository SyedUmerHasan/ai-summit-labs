"""
Lab 03 — Agents as Tools
04: Proposal Writer — write a technical/business proposal from requirements
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read, http_request
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="proposal-writer",
    storage_dir=SESSIONS_DIR,
)

researcher = Agent(
    model=get_model(),
    name="researcher",
    system_prompt="You are a technical researcher. Given a topic, gather key facts, industry context, and relevant data points to support a proposal. Plain text, no markdown.",
)

writer = Agent(
    model=get_model(),
    name="writer",
    system_prompt="You are a proposal writer. Given research and requirements, write a clear, persuasive proposal with: problem statement, proposed solution, benefits, timeline, and budget. Plain text, no markdown.",
)

reviewer = Agent(
    model=get_model(),
    name="reviewer",
    system_prompt="You are a proposal reviewer. Given a draft proposal, identify weaknesses, missing sections, unclear points, and suggest improvements. Plain text, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[researcher, writer, reviewer, file_read, file_write, http_request],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are a proposal lead. When asked to write a proposal:
1. Ask researcher for background and context
2. Ask writer to draft the proposal
3. Ask reviewer to critique it
Deliver the final polished proposal. You can save output to a file using file_write when asked.
Plain text, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Proposal Writer — Lab 03")
