"""
Lab 02 — Stateful Agent
04: User Preferences — agent learns and remembers your preferences
"""
import os
from strands import Agent, tool, ToolContext
from strands.session.file_session_manager import FileSessionManager
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="prefs-session",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = """You are a personal assistant that adapts to user preferences.
You remember the user's name, communication style, interests, and settings.
When you learn something new about the user, save it with set_preference.
Always check preferences before responding to personalize your answers.
Respond in plain text, no markdown."""


@tool(context=True)
def set_preference(key: str, value: str, tool_context: ToolContext) -> str:
    """Save a user preference.

    Args:
        key: Preference name (e.g., "name", "tone", "interests").
        value: Preference value.
    """
    prefs = tool_context.agent.state.get("preferences") or {}
    prefs[key] = value
    tool_context.agent.state.set("preferences", prefs)
    return f"Preference saved: {key} = {value}"


@tool(context=True)
def get_preferences(tool_context: ToolContext) -> str:
    """Get all saved user preferences."""
    prefs = tool_context.agent.state.get("preferences") or {}
    if not prefs:
        return "No preferences saved yet."
    return "\n".join(f"  {k}: {v}" for k, v in prefs.items())


agent = Agent(
    model=get_model(),
    tools=[set_preference, get_preferences],
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
    state={"preferences": {}},
)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="User Preferences — Lab 02")
