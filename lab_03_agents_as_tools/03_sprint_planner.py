"""
Lab 03 — Agents as Tools
03: Sprint Planner — distribute work across team for a quarter
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="sprint-planner",
    storage_dir=SESSIONS_DIR,
)

capacity_planner = Agent(
    model=get_model(),
    name="capacity_planner",
    system_prompt="You are a capacity planner. Given team size, skills, and time-off, calculate available capacity per sprint. Plain text, no markdown.",
)

work_distributor = Agent(
    model=get_model(),
    name="work_distributor",
    system_prompt="You are a work distributor. Given tasks with estimates and team capacity, assign tasks to team members balancing load and skills. Plain text, no markdown.",
)

timeline_builder = Agent(
    model=get_model(),
    name="timeline_builder",
    system_prompt="You are a timeline builder. Given sprint assignments, create a quarter-level timeline showing milestones and dependencies. Plain text, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[capacity_planner, work_distributor, timeline_builder, file_read, file_write],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are an engineering manager planning a quarter. When asked:
1. Ask capacity_planner for team availability
2. Ask work_distributor to assign work across the team
3. Ask timeline_builder for the quarterly timeline
Deliver a complete sprint plan. You can save output to a file using file_write when asked.
Plain text, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Sprint Planner — Lab 03")
