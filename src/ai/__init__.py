"""AI integration module"""

from .manager import AIManager
from .local_client import LocalAIClient
from .online_clients import OpenAIClient, AnthropicClient, GoogleClient
from .prompt_templates import PromptTemplates

__all__ = [
    'AIManager',
    'LocalAIClient',
    'OpenAIClient',
    'AnthropicClient',
    'GoogleClient',
    'PromptTemplates'
]
