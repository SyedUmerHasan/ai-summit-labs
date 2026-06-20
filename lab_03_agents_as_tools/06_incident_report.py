"""
Lab 03 — Agents as Tools
06: Incident Report — generate a post-mortem from raw incident data
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read, shell
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="incident-report",
    storage_dir=SESSIONS_DIR,
)

timeline_builder = Agent(
    model=get_model(),
    name="timeline_builder",
    system_prompt="You are a timeline builder. Given raw incident data (alerts, logs, messages), construct a chronological timeline of events. Plain text, no markdown.",
)

root_cause_analyzer = Agent(
    model=get_model(),
    name="root_cause_analyzer",
    system_prompt="You are a root cause analyst. Given an incident timeline, identify the root cause using 5-whys analysis. Plain text, no markdown.",
)

report_writer = Agent(
    model=get_model(),
    name="report_writer",
    system_prompt="You are a post-mortem writer. Given timeline and root cause, write a structured incident report with: summary, impact, timeline, root cause, corrective actions, and lessons learned. Plain text, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[timeline_builder, root_cause_analyzer, report_writer, file_read, file_write, shell],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are an incident commander. When asked to write a post-mortem:
1. Ask timeline_builder to construct the event timeline
2. Ask root_cause_analyzer to identify why it happened
3. Ask report_writer to produce the final report
Deliver a complete post-mortem. You can save output to a file using file_write when asked.
Plain text, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Incident Report — Lab 03")
