"""
Lab 03 — Agents as Tools
02: User Stories — generate user stories from a product idea
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="user-stories",
    storage_dir=SESSIONS_DIR,
)

feature_analyst = Agent(
    model=get_model(),
    name="feature_analyst",
    system_prompt="You are a feature analyst. Given a product idea, identify the key user personas and their needs. Plain text, no markdown.",
)

story_writer = Agent(
    model=get_model(),
    name="story_writer",
    system_prompt="You are a user story writer. Given personas and needs, write user stories in the format: As a [persona], I want [goal], so that [benefit]. Include edge cases. Plain text, no markdown.",
)

criteria_checker = Agent(
    model=get_model(),
    name="criteria_checker",
    system_prompt="You are a QA specialist. Given user stories, add detailed acceptance criteria and test scenarios for each. Plain text, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[feature_analyst, story_writer, criteria_checker, file_read, file_write],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are a product manager. When asked to create user stories:
1. Ask feature_analyst to identify personas and needs
2. Ask story_writer to write the user stories
3. Ask criteria_checker to add acceptance criteria
Deliver the complete set of stories. You can save output to a file using file_write when asked.
Plain text, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="User Stories — Lab 03")
