"""
Provider Module
Contains provider classes for external integrations
"""

from .base_provider import BaseProvider
from .ollama_provider import OllamaProvider

__all__ = ['BaseProvider', 'OllamaProvider']

