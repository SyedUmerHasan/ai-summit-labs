"""
Lab 02 — Stateful Agent
05: Multi Session — multiple users with isolated sessions
Run with: python3 05_multi_session.py <username>
Each user gets their own conversation history and state.
"""
import os
import sys
from strands import Agent, tool, ToolContext
from strands.session.file_session_manager import FileSessionManager
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

username = sys.argv[1] if len(sys.argv) > 1 else "default-user"

session_manager = FileSessionManager(
    session_id=f"user-{username}",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = f"""You are a personal assistant for {username}.
You remember this user's conversation history and preferences.
Always address them by name. Each user has isolated state.
Respond in plain text, no markdown."""


@tool(context=True)
def whoami(tool_context: ToolContext) -> str:
    """Show current session info."""
    prefs = tool_context.agent.state.get("preferences") or {}
    return f"Session: user-{username}\nUser: {username}\nPreferences: {prefs}"


@tool(context=True)
def set_preference(key: str, value: str, tool_context: ToolContext) -> str:
    """Save a preference for this user.

    Args:
        key: Preference name.
        value: Preference value.
    """
    prefs = tool_context.agent.state.get("preferences") or {}
    prefs[key] = value
    tool_context.agent.state.set("preferences", prefs)
    return f"Saved: {key} = {value}"


agent = Agent(
    model=get_model(),
    tools=[whoami, set_preference],
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
    state={"preferences": {}},
)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title=f"Multi Session ({username}) — Lab 02")
