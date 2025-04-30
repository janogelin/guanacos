"""
Interactive Ollama chat application with command history navigation.
"""

from .app import OllamaChatApp, main
from .command_history import CommandHistory
from .interactive_prompt import InteractivePrompt
from .ollama_client import OllamaClient

__version__ = "0.1.0"
__all__ = ['OllamaChatApp', 'CommandHistory', 'InteractivePrompt', 'OllamaClient', 'main'] 