"""
Terminal engine for all labs.
Uses `rich` for styled rendering in terminal.
"""
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.padding import Padding
from rich.rule import Rule
from rich.text import Text

console = Console()

GREEN = "\033[32m"
RESET = "\033[0m"

_seen_tool_ids = set()
_buffer = []


def callback_handler(**kwargs):
    """Custom callback handler — buffers text, shows tools inline."""
    global _seen_tool_ids, _buffer

    # Thinking / reasoning
    if kwargs.get("reasoning"):
        text = kwargs.get("reasoningText", "")
        if text:
            console.print(Text(text, style="dim italic"))
        return

    # Streamed text — buffer for rich rendering
    if "data" in kwargs:
        _buffer.append(kwargs["data"])
        return

    # Tool use
    if "current_tool_use" in kwargs:
        tool = kwargs["current_tool_use"]
        tool_id = tool.get("toolUseId", "")
        name = tool.get("name", "")
        if name and tool_id not in _seen_tool_ids:
            _seen_tool_ids.add(tool_id)
            inp = tool.get("input", {})

            _flush_buffer()

            if isinstance(inp, dict):
                detail = inp.get("command") or inp.get("path") or inp.get("url") or inp.get("action") or ""
                if isinstance(detail, str):
                    detail = detail[:80]
            elif isinstance(inp, str):
                detail = inp[:80]
            else:
                detail = ""

            console.print(f"  [yellow]● {name}[/yellow] [dim]{detail}[/dim]")
            console.print()
        return


def _flush_buffer():
    """Render buffered AI response with colored left border style."""
    global _buffer
    if _buffer:
        text = "".join(_buffer)
        _buffer = []
        if text.strip():
            # Render markdown then print with left colored bar using padding
            console.print()
            for line in text.split("\n"):
                if line.strip():
                    console.print(Text("│ ", style="bold cyan"), end="")
                    console.print(Text(line, style="italic"))
                else:
                    console.print(Text("│", style="bold cyan"))
            console.print()


def run_chat(agent, title="Agent"):
    """Interactive terminal chat loop. Accepts Agent, Graph, Swarm, or any callable."""
    global _seen_tool_ids, _buffer

    console.print(f"\n[bold cyan]  {title}[/bold cyan]")
    console.print(f"[dim]  Type 'q' to quit[/dim]\n")

    try:
        while True:
            _seen_tool_ids = set()
            _buffer = []
            message = input(f"{GREEN}> {RESET}").strip()
            if not message:
                continue
            if message.lower() in ("q", "quit", "exit"):
                break
            print()
            agent(message)
            _flush_buffer()
            print()
            console.print(Rule(style="dim"))
            print()
    except (KeyboardInterrupt, EOFError):
        pass
