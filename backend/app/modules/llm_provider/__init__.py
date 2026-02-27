"""
LLM Provider Module — Llama integration for AIComplianceGuard.
Supports llama-cpp-python (GGUF) and HuggingFace transformers backends.
"""

from app.modules.llm_provider.provider import LLMProvider, llm_provider

__all__ = ["LLMProvider", "llm_provider"]
