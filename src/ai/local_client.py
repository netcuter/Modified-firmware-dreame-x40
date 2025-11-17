"""Local AI Client (LM Studio compatible)"""

import httpx
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class LocalAIClient:
    """Client for local AI models (LM Studio, Ollama, etc.)

    Uses OpenAI-compatible API that LM Studio provides.
    """

    def __init__(
        self,
        base_url: str,
        model: str = "local-model",
        timeout: int = 30,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """Initialize local AI client

        Args:
            base_url: Base URL of local AI server (e.g., http://192.168.1.50:1234/v1)
            model: Model name (for LM Studio, can be "local-model")
            timeout: Request timeout in seconds
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.client = httpx.AsyncClient(timeout=timeout)
        logger.info(f"Initialized LocalAIClient: {base_url}")

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def check_health(self) -> bool:
        """Check if local AI server is healthy

        Returns:
            True if server is reachable and responding
        """
        try:
            # Try to get models list
            response = await self.client.get(f"{self.base_url}/models")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Get chat completion from local model

        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            max_tokens: Override max_tokens
            temperature: Override temperature

        Returns:
            Model response text

        Raises:
            Exception if request fails
        """
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature or self.temperature,
            "stream": False
        }

        logger.debug(f"Sending chat completion request: {len(messages)} messages")

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            logger.debug(f"Received response: {content[:100]}...")
            return content

        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise Exception(f"Local AI request failed: {e}")
        except KeyError as e:
            logger.error(f"Invalid response format: {e}")
            raise Exception(f"Invalid response from local AI: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    async def simple_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Simple prompt completion

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt

        Returns:
            Model response
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        return await self.chat_completion(messages)

    async def get_models(self) -> List[str]:
        """Get list of available models

        Returns:
            List of model names
        """
        try:
            response = await self.client.get(f"{self.base_url}/models")
            response.raise_for_status()

            data = response.json()
            models = [model["id"] for model in data.get("data", [])]

            logger.debug(f"Available models: {models}")
            return models

        except Exception as e:
            logger.error(f"Failed to get models: {e}")
            return []
