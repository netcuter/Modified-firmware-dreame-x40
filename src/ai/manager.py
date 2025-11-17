"""AI Manager - Manages AI model selection and fallback"""

import logging
from typing import List, Dict, Any, Optional
from enum import Enum

from .local_client import LocalAIClient
from .online_clients import OpenAIClient, AnthropicClient, GoogleClient
from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """AI model types"""
    LOCAL = "local"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class AIManager:
    """Manages AI models and handles fallback"""

    def __init__(self, config):
        """Initialize AI manager

        Args:
            config: AIConfig object from settings
        """
        self.config = config
        self.current_model = ModelType(config.default_model)
        self.language = config.language
        self.auto_fallback = config.auto_fallback

        # Initialize clients
        self.local_client: Optional[LocalAIClient] = None
        self.openai_client: Optional[OpenAIClient] = None
        self.anthropic_client: Optional[AnthropicClient] = None
        self.google_client: Optional[GoogleClient] = None

        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 20

        logger.info(f"Initialized AIManager (default: {self.current_model.value})")

    async def initialize(self):
        """Initialize AI clients based on configuration"""

        # Initialize local client
        if self.config.local.enabled:
            try:
                self.local_client = LocalAIClient(
                    base_url=self.config.local.base_url,
                    model=self.config.local.model,
                    timeout=self.config.local.timeout,
                    max_tokens=self.config.local.max_tokens,
                    temperature=self.config.local.temperature
                )
                # Check if local server is available
                is_healthy = await self.local_client.check_health()
                if is_healthy:
                    logger.info("Local AI client initialized and healthy")
                else:
                    logger.warning("Local AI client not responding")
                    if self.current_model == ModelType.LOCAL and self.auto_fallback:
                        logger.info("Switching to online model")
                        self.current_model = ModelType(self.config.online.default_provider)
            except Exception as e:
                logger.error(f"Failed to initialize local AI client: {e}")
                if self.current_model == ModelType.LOCAL and self.auto_fallback:
                    self.current_model = ModelType(self.config.online.default_provider)

        # Initialize OpenAI client
        if self.config.online.openai.enabled and self.config.online.openai.api_key:
            try:
                self.openai_client = OpenAIClient(
                    api_key=self.config.online.openai.api_key,
                    model=self.config.online.openai.model,
                    base_url=self.config.online.openai.base_url,
                    max_tokens=self.config.online.openai.max_tokens,
                    temperature=self.config.online.openai.temperature
                )
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")

        # Initialize Anthropic client
        if self.config.online.anthropic.enabled and self.config.online.anthropic.api_key:
            try:
                self.anthropic_client = AnthropicClient(
                    api_key=self.config.online.anthropic.api_key,
                    model=self.config.online.anthropic.model,
                    max_tokens=self.config.online.anthropic.max_tokens,
                    temperature=self.config.online.anthropic.temperature
                )
                logger.info("Anthropic client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")

        # Initialize Google client
        if self.config.online.google.enabled and self.config.online.google.api_key:
            try:
                self.google_client = GoogleClient(
                    api_key=self.config.online.google.api_key,
                    model=self.config.online.google.model,
                    max_tokens=self.config.online.google.max_tokens,
                    temperature=self.config.online.google.temperature
                )
                logger.info("Google client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google client: {e}")

    async def close(self):
        """Close all AI clients"""
        if self.local_client:
            await self.local_client.close()
        if self.openai_client:
            await self.openai_client.close()
        if self.anthropic_client:
            await self.anthropic_client.close()
        if self.google_client:
            await self.google_client.close()

    def switch_model(self, model_type: str):
        """Switch to different model

        Args:
            model_type: "local", "openai", "anthropic", or "google"
        """
        try:
            new_model = ModelType(model_type)
            self.current_model = new_model
            logger.info(f"Switched to model: {model_type}")
        except ValueError:
            logger.error(f"Invalid model type: {model_type}")
            raise ValueError(f"Invalid model type: {model_type}")

    def get_current_model(self) -> str:
        """Get current model type

        Returns:
            Current model type as string
        """
        return self.current_model.value

    async def chat(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        add_to_history: bool = True
    ) -> str:
        """Send chat message to AI

        Args:
            message: User message
            context: Optional context (robot status, rooms, etc.)
            add_to_history: Whether to add to conversation history

        Returns:
            AI response
        """
        # Get system prompt
        system_prompt = PromptTemplates.get_system_prompt(self.language)

        # Format message with context
        formatted_message = PromptTemplates.format_user_message(message, context)

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        messages.extend(self.conversation_history[-self.max_history:])

        # Add current message
        messages.append({"role": "user", "content": formatted_message})

        # Try to get response from current model
        response = None
        fallback_attempted = False

        while response is None:
            try:
                response = await self._get_completion(messages)
                break
            except Exception as e:
                logger.error(f"Failed to get response from {self.current_model.value}: {e}")

                # Try fallback if enabled
                if self.auto_fallback and not fallback_attempted:
                    logger.info("Attempting fallback to alternative model")
                    if self.current_model == ModelType.LOCAL:
                        # Fallback to online
                        self.current_model = ModelType(self.config.online.default_provider)
                    else:
                        # Try local if available
                        if self.local_client:
                            self.current_model = ModelType.LOCAL
                        else:
                            raise Exception("All models failed")

                    fallback_attempted = True
                else:
                    raise Exception(f"AI request failed: {e}")

        # Add to history if requested
        if add_to_history:
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response})

        return response

    async def _get_completion(self, messages: List[Dict[str, str]]) -> str:
        """Get completion from current model

        Args:
            messages: Message history

        Returns:
            AI response

        Raises:
            Exception if request fails
        """
        if self.current_model == ModelType.LOCAL:
            if not self.local_client:
                raise Exception("Local AI client not initialized")
            return await self.local_client.chat_completion(messages)

        elif self.current_model == ModelType.OPENAI:
            if not self.openai_client:
                raise Exception("OpenAI client not initialized")
            return await self.openai_client.chat_completion(messages)

        elif self.current_model == ModelType.ANTHROPIC:
            if not self.anthropic_client:
                raise Exception("Anthropic client not initialized")
            return await self.anthropic_client.chat_completion(messages)

        elif self.current_model == ModelType.GOOGLE:
            if not self.google_client:
                raise Exception("Google client not initialized")
            return await self.google_client.chat_completion(messages)

        else:
            raise Exception(f"Unknown model type: {self.current_model}")

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history

        Returns:
            List of message dicts
        """
        return self.conversation_history.copy()

    def get_available_models(self) -> List[str]:
        """Get list of available models

        Returns:
            List of model type strings
        """
        models = []

        if self.local_client:
            models.append("local")
        if self.openai_client:
            models.append("openai")
        if self.anthropic_client:
            models.append("anthropic")
        if self.google_client:
            models.append("google")

        return models
