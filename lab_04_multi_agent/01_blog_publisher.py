"""
Lab 04 — Multi-Agent Orchestration
01: Blog Publisher — Sequential Workflow Architecture

Pattern: Agents process tasks in order. Each agent's output becomes input for the next.
Sub-agents have callback_handler=None (silent). Only the final output is shown.
"""
import os

from strands import Agent
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import file_write, shell
from shared.model_config import get_model
from shared.tools import read_document
from shared.terminal import callback_handler, run_chat

# Specialized agents (silent — output captured, not printed)
researcher = Agent(
    model=get_model(),
    system_prompt="You are a research specialist. Find key facts, statistics, and angles on the topic. Plain text only.",
    callback_handler=None,
)

writer = Agent(
    model=get_model(),
    system_prompt="You are a blog writer. Write an engaging 500-word blog post based on the research provided. Plain text only.",
    callback_handler=None,
)

seo_optimizer = Agent(
    model=get_model(),
    system_prompt="You are an SEO specialist. Optimize the blog post: add a compelling title, meta description, and 5 target keywords. Return the complete optimized post. Plain text only.",
    callback_handler=None,
)


def run_blog_workflow(topic: str) -> str:
    """Sequential workflow: research → write → SEO optimize."""
    print("  [1/3] Researching...")
    research_results = researcher(f"Research this topic for a blog post: {topic}")

    print("  [2/3] Writing draft...")
    draft = writer(f"Write a blog post based on this research:\n{research_results.message}")

    print("  [3/3] SEO optimizing...")
    final = seo_optimizer(f"Optimize this blog post for SEO:\n{draft.message}")

    return final.message


# Coordinator agent — handles user interaction, file operations
coordinator = Agent(
    model=get_model(),
    tools=[file_write, shell, read_document],
    system_prompt="""You are a blog publishing assistant.
When the user asks you to write/create a blog post, the workflow has already run and the result is provided to you.
Your job: show the result and ask where to save it. Use shell for pwd/ls, file_write to save.
If given a document, use read_document first.
Plain text output, no markdown.""",
    callback_handler=callback_handler,
    interventions=[HumanInTheLoop(ask="stdio", allowed_tools=["shell", "read_document"])],
)


def invoke(message: str, history: list = None):
    if any(kw in message.lower() for kw in ["write", "blog", "post", "article", "create"]):
        result = run_blog_workflow(message)
        return coordinator(f"Blog post ready. Show it to the user and ask where to save:\n\n{result}")
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Blog Publisher (Sequential Workflow) — Lab 04")
