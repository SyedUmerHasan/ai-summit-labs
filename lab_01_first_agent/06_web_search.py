"""
Lab 01 — Your First Agent
06: Web Search via MCP (DuckDuckGo — no API key needed)

Prerequisites: pip install mcp && curl -LsSf https://astral.sh/uv/install.sh | sh
"""
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from shared.model_config import get_model
from shared.terminal import callback_handler, run_chat
from strands.tools.mcp import MCPClient

SYSTEM_PROMPT = """You are a personal assistant with web search.
For normal chat, just respond. Only search when the user asks to look something up.
Respond in plain text, no markdown."""

search_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx", args=["duckduckgo-mcp-server"])
))

agent = Agent(model=get_model(), tools=[search_client], system_prompt=SYSTEM_PROMPT, callback_handler=callback_handler)


def invoke(message: str, history: list = None):
    return agent(message)


if __name__ == "__main__":
    run_chat(agent, title="Web Search Agent — Lab 01")
