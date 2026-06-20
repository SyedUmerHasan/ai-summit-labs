"""
Lab 02 — Stateful Agent
02: Personal Notes — add, search, and list notes that persist across sessions
"""
import os
from strands import Agent, tool, ToolContext
from strands.session.file_session_manager import FileSessionManager
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="notes-session",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = """You are a personal notes assistant. You can save, search, and list notes.
Notes persist across sessions. Help the user organize their thoughts.
For normal chat, respond naturally. Use tools only when the user wants to manage notes.
Respond in plain text, no markdown."""


@tool(context=True)
def add_note(title: str, content: str, tool_context: ToolContext) -> str:
    """Save a new note.

    Args:
        title: Short title for the note.
        content: The note content.
    """
    notes = tool_context.agent.state.get("notes") or []
    notes.append({"title": title, "content": content})
    tool_context.agent.state.set("notes", notes)
    return f"Note saved: '{title}' ({len(notes)} total notes)"


@tool(context=True)
def list_notes(tool_context: ToolContext) -> str:
    """List all saved notes."""
    notes = tool_context.agent.state.get("notes") or []
    if not notes:
        return "No notes saved yet."
    return "\n".join(f"{i+1}. {n['title']} - {n['content'][:50]}" for i, n in enumerate(notes))


@tool(context=True)
def search_notes(query: str, tool_context: ToolContext) -> str:
    """Search notes by keyword.

    Args:
        query: Keyword to search for in notes.
    """
    notes = tool_context.agent.state.get("notes") or []
    matches = [n for n in notes if query.lower() in n["title"].lower() or query.lower() in n["content"].lower()]
    if not matches:
        return f"No notes found matching '{query}'."
    return "\n".join(f"- {n['title']}: {n['content']}" for n in matches)


agent = Agent(
    model=get_model(),
    tools=[add_note, list_notes, search_notes],
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
    state={"notes": []},
)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Personal Notes — Lab 02")
