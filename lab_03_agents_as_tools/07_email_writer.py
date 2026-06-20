"""
Lab 03 — Agents as Tools
07: Email Writer — draft professional emails from context and intent
"""
import os
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_write, file_read
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="email-writer",
    storage_dir=SESSIONS_DIR,
)

tone_analyzer = Agent(
    model=get_model(),
    name="tone_analyzer",
    system_prompt="You are a communication tone analyzer. Given the context (who, what, why), determine the appropriate tone: formal, friendly, urgent, apologetic, persuasive, etc. Plain text, no markdown.",
)

drafter = Agent(
    model=get_model(),
    name="drafter",
    system_prompt="You are an email drafter. Given context and tone, write a clear professional email with subject line, greeting, body, and sign-off. Plain text, no markdown.",
)

polisher = Agent(
    model=get_model(),
    name="polisher",
    system_prompt="You are an email editor. Given a draft email, improve clarity, fix grammar, tighten wording, and ensure the tone is appropriate. Return the final version. Plain text, no markdown.",
)

coordinator = Agent(
    model=get_model(),
    tools=[tone_analyzer, drafter, polisher, file_read, file_write],
    callback_handler=callback_handler,
    session_manager=session_manager,
    system_prompt="""You are a communication assistant. When asked to write an email:
1. Ask tone_analyzer for the right tone given the context
2. Ask drafter to write the email
3. Ask polisher to refine it
Deliver the final email ready to send. You can save output to a file using file_write when asked.
Plain text, no markdown.""",
)


def invoke(message: str, history: list = None):
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Email Writer — Lab 03")
