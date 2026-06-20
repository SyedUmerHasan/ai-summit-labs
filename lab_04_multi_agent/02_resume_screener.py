"""
Lab 04 — Multi-Agent Orchestration
02: Resume Screener — Sequential Workflow with Context Passing

Pattern: Each agent builds on the previous agent's output.
Uses read_document to convert PDF/DOCX before processing.
"""
import os

from strands import Agent
from strands.vended_interventions.hitl import HumanInTheLoop
from strands_tools import file_write, shell
from shared.model_config import get_model
from shared.tools import read_document
from shared.terminal import callback_handler, run_chat

# Specialized agents (silent)
parser = Agent(
    model=get_model(),
    system_prompt="You parse resumes. Extract: name, contact, skills, years of experience, roles held, education, certifications. Structured plain text only.",
    callback_handler=None,
)

matcher = Agent(
    model=get_model(),
    system_prompt="You match resumes to jobs. Given parsed resume data and a job description, score 0-100 and list strengths, gaps, and deal-breakers. Plain text only.",
    callback_handler=None,
)

report_writer = Agent(
    model=get_model(),
    system_prompt="You write HR screening reports. Given a match analysis, produce: score, recommendation (proceed/reject/maybe), key highlights, concerns. Plain text only.",
    callback_handler=None,
)


def run_screening_workflow(resume_text: str, job_description: str = "") -> str:
    """Sequential workflow: parse → match → report."""
    print("  [1/3] Parsing resume...")
    parsed = parser(f"Parse this resume:\n{resume_text}")

    print("  [2/3] Matching against job description...")
    job_ctx = f"\n\nJob Description:\n{job_description}" if job_description else "\n\nNo specific job description provided. Do a general assessment."
    matched = matcher(f"Match this parsed resume against the job:\n\nResume Data:\n{parsed.message}{job_ctx}")

    print("  [3/3] Writing screening report...")
    report = report_writer(f"Write a screening report based on this analysis:\n{matched.message}")

    return report.message


# Coordinator agent
coordinator = Agent(
    model=get_model(),
    tools=[file_write, shell, read_document],
    system_prompt="""You are an HR screening assistant.
When the user provides a resume (file path or text), you:
1. Use read_document to convert PDF/DOCX to text if a file path is given
2. Ask for a job description if not provided
3. The screening workflow runs automatically and gives you the report
4. Show the report and ask where to save (file_write or create_pdf)

Use shell for pwd/ls. Plain text output, no markdown.""",
    callback_handler=callback_handler,
    interventions=[HumanInTheLoop(ask="stdio", allowed_tools=["shell", "read_document"])],
)


def invoke(message: str, history: list = None):
    # If it looks like a file path, convert first
    if any(ext in message for ext in [".pdf", ".docx", ".doc", ".txt"]):
        import subprocess
        path = message.strip().strip("'\"")
        try:
            result = subprocess.run(["markitdown", path], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                resume_text = result.stdout
                report = run_screening_workflow(resume_text)
                return coordinator(f"Screening report ready:\n\n{report}\n\nAsk user where to save.")
        except Exception:
            pass
    return coordinator(message)


if __name__ == "__main__":
    run_chat(coordinator, title="Resume Screener (Sequential Workflow) — Lab 04")
