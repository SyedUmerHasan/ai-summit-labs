"""
Shared package — auto-initializes Langfuse observability.
All labs get tracing automatically by importing from shared.
"""
import os

if os.getenv("LANGFUSE_PUBLIC_KEY"):
    try:
        from langfuse import get_client
        _langfuse = get_client()
    except ImportError:
        pass
