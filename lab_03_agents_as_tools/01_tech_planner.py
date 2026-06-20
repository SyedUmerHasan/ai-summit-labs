"""
Lab 03 — Agents as Tools
01: Tech Planner — break a feature into architecture, tasks, and estimates
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="tech-planner",
    storage_dir=SESSIONS_DIR,
)

architect = Agent(
    model=get_model(),
    name="architect",
    system_prompt="You are a software architect. Given a feature request, define the system design: components, data flow, APIs, and tech stack. Plain text output, no markdown.",
)

task_planner = Agent(
    model=get_model(),
    name="task_planner",
    system_prompt="You are a task planner. Given a system design, break it into individual dev tasks with clear acceptance criteria. Plain text output, no markdown.",
)

estimator = Agent(
    model=get_model(),
    name="estimator",
    system_prompt="You are a project estimator. Given a list of tasks, estimate hours for each and provide a total. Be realistic. Plain text output, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[architect, task_planner, estimator, file_read, file_write],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are a tech lead. When asked to plan a feature:
1. Ask architect for the system design
2. Ask task_planner to break it into tasks
3. Ask estimator for time estimates
Combine into a final technical plan.
You can also save output to a file using file_write when the user asks.
For normal chat, just respond. Plain text output, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Tech Planner — Lab 03")
