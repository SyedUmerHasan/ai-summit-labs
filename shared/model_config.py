"""
Shared model factory for all labs.
Usage: MODEL=ollama python3 lab_01/01_basic_agent.py
   or: get_model(ModelProvider.BEDROCK, "us.anthropic.claude-haiku-4-5")
"""
import os
from enum import Enum


class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    QWEN = "qwen"
    BEDROCK = "bedrock"
    ANTHROPIC = "anthropic"


def get_model(provider: ModelProvider = None, model_id: str = None):
    provider = provider or ModelProvider(os.getenv("MODEL", "anthropic"))

    match provider:
        case ModelProvider.OLLAMA:
            from strands.models.ollama import OllamaModel
            return OllamaModel(
                host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                model_id=model_id or "llama3.1",
            )

        case ModelProvider.QWEN:
            from strands.models.ollama import OllamaModel
            return OllamaModel(
                host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                model_id=model_id or "qwen2.5:7b",
            )

        case ModelProvider.BEDROCK:
            from strands.models import BedrockModel
            return BedrockModel(
                model_id=model_id or "us.anthropic.claude-sonnet-4-5",
                region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            )

        case ModelProvider.ANTHROPIC:
            from strands.models.anthropic import AnthropicModel
            return AnthropicModel(
                model_id=model_id or "claude-haiku-4-5-20251001",
                max_tokens=16000,
            )
