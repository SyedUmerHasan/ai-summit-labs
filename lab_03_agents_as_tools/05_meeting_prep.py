"""
Lab 03 — Agents as Tools
05: Meeting Prep — prepare agenda and talking points from context
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="meeting-prep",
    storage_dir=SESSIONS_DIR,
)

context_analyzer = Agent(
    model=get_model(),
    name="context_analyzer",
    system_prompt="You are a context analyzer. Given meeting participants and topic, identify key discussion points, potential conflicts, and decisions needed. Plain text, no markdown.",
)

agenda_builder = Agent(
    model=get_model(),
    name="agenda_builder",
    system_prompt="You are an agenda builder. Given discussion points, create a timed agenda with clear objectives for each section. Plain text, no markdown.",
)

action_tracker = Agent(
    model=get_model(),
    name="action_tracker",
    system_prompt="You are an action item tracker. Given an agenda, pre-populate likely action items and owners based on the topic. Plain text, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[context_analyzer, agenda_builder, action_tracker, file_read, file_write],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are a meeting organizer. When asked to prepare for a meeting:
1. Ask context_analyzer to identify key points and decisions
2. Ask agenda_builder to create a timed agenda
3. Ask action_tracker to suggest likely action items
Deliver a complete meeting prep package. You can save output to a file using file_write when asked.
Plain text, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Meeting Prep — Lab 03")
