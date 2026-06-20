"""
Shared tools: document reading.
"""
import subprocess
from strands import tool


@tool
def read_document(file_path: str) -> str:
    """Read and convert a document (PDF, DOCX, PPTX, Excel, etc.) to plain text.

    Args:
        file_path: Path to the document file.
    """
    try:
        result = subprocess.run(
            ["markitdown", file_path],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return f"Error reading document: {result.stderr}"
        return result.stdout
    except FileNotFoundError:
        return "Error: markitdown not installed. Run: pip install 'markitdown[all]'"
    except subprocess.TimeoutExpired:
        return "Error: document conversion timed out."
