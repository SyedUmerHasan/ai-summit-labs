"""
Lab 02 — Stateful Agent
03: Todo Tracker — manages tasks with status, persists across sessions
"""
import os
from strands import Agent, tool, ToolContext
from strands.session.file_session_manager import FileSessionManager
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")

session_manager = FileSessionManager(
    session_id="todo-session",
    storage_dir=SESSIONS_DIR,
)

SYSTEM_PROMPT = """You are a task management assistant. You track to-do items with status.
Tasks persist across sessions. Help users add, complete, and review tasks.
For normal chat, respond naturally. Use tools when managing tasks.
Respond in plain text, no markdown."""


@tool(context=True)
def add_task(title: str, priority: str, tool_context: ToolContext) -> str:
    """Add a new task.

    Args:
        title: Task description.
        priority: Priority level — high, medium, or low.
    """
    tasks = tool_context.agent.state.get("tasks") or []
    task = {"id": len(tasks) + 1, "title": title, "priority": priority, "done": False}
    tasks.append(task)
    tool_context.agent.state.set("tasks", tasks)
    return f"Task #{task['id']} added: {title} [{priority}]"


@tool(context=True)
def complete_task(task_id: int, tool_context: ToolContext) -> str:
    """Mark a task as complete.

    Args:
        task_id: The ID of the task to complete.
    """
    tasks = tool_context.agent.state.get("tasks") or []
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            tool_context.agent.state.set("tasks", tasks)
            return f"Task #{task_id} marked complete: {t['title']}"
    return f"Task #{task_id} not found."


@tool(context=True)
def list_tasks(tool_context: ToolContext) -> str:
    """List all tasks with their status."""
    tasks = tool_context.agent.state.get("tasks") or []
    if not tasks:
        return "No tasks yet."
    lines = []
    for t in tasks:
        status = "done" if t["done"] else "todo"
        lines.append(f"  [{status}] #{t['id']} [{t['priority']}] {t['title']}")
    return "\n".join(lines)


agent = Agent(
    model=get_model(),
    tools=[add_task, complete_task, list_tasks],
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    callback_handler=callback_handler,
    state={"tasks": []},
)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Todo Tracker — Lab 02")
