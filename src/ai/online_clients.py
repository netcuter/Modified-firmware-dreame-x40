"""Online AI Clients (OpenAI, Anthropic, Google)"""

import logging
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for OpenAI API (GPT-4, GPT-3.5)"""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        base_url: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """Initialize OpenAI client

        Args:
            api_key: OpenAI API key
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
            base_url: Optional custom base URL
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        if base_url:
            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = AsyncOpenAI(api_key=api_key)

        logger.info(f"Initialized OpenAIClient: {model}")

    async def close(self):
        """Close client"""
        await self.client.close()

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Get chat completion

        Args:
            messages: List of message dicts
            max_tokens: Override max_tokens
            temperature: Override temperature

        Returns:
            Model response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature
            )

            content = response.choices[0].message.content
            logger.debug(f"OpenAI response: {content[:100]}...")
            return content

        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise Exception(f"OpenAI request failed: {e}")

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


class AnthropicClient:
    """Client for Anthropic API (Claude)"""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """Initialize Anthropic client

        Args:
            api_key: Anthropic API key
            model: Model name (e.g., "claude-3-5-sonnet-20241022")
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = AsyncAnthropic(api_key=api_key)

        logger.info(f"Initialized AnthropicClient: {model}")

    async def close(self):
        """Close client"""
        await self.client.close()

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """Get chat completion

        Args:
            messages: List of message dicts (without system message)
            max_tokens: Override max_tokens
            temperature: Override temperature
            system_prompt: System prompt (Claude uses separate parameter)

        Returns:
            Model response text
        """
        try:
            # Filter out system messages (Claude handles them separately)
            user_messages = [m for m in messages if m["role"] != "system"]

            # Extract system prompt if in messages
            if not system_prompt:
                system_messages = [m for m in messages if m["role"] == "system"]
                if system_messages:
                    system_prompt = system_messages[0]["content"]

            kwargs = {
                "model": self.model,
                "messages": user_messages,
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature or self.temperature
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = await self.client.messages.create(**kwargs)

            content = response.content[0].text
            logger.debug(f"Claude response: {content[:100]}...")
            return content

        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise Exception(f"Anthropic request failed: {e}")

    async def simple_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Simple prompt completion

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt

        Returns:
            Model response
        """
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, system_prompt=system_prompt)


class GoogleClient:
    """Client for Google Generative AI (Gemini)"""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """Initialize Google Gemini client

        Args:
            api_key: Google API key
            model: Model name (e.g., "gemini-pro")
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        """
        self.model_name = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

        logger.info(f"Initialized GoogleClient: {model}")

    async def close(self):
        """Close client (no-op for Google)"""
        pass

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Get chat completion

        Args:
            messages: List of message dicts
            max_tokens: Override max_tokens
            temperature: Override temperature

        Returns:
            Model response text
        """
        try:
            # Convert messages to Gemini format
            # System message becomes part of the first user message
            system_prompt = ""
            user_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                elif msg["role"] == "user":
                    content = msg["content"]
                    if system_prompt:
                        content = f"{system_prompt}\n\n{content}"
                        system_prompt = ""  # Only add once
                    user_messages.append({"role": "user", "parts": [content]})
                elif msg["role"] == "assistant":
                    user_messages.append({"role": "model", "parts": [msg["content"]]})

            # For single message, use generate_content
            if len(user_messages) == 1:
                response = await self.model.generate_content_async(
                    user_messages[0]["parts"][0],
                    generation_config={
                        "max_output_tokens": max_tokens or self.max_tokens,
                        "temperature": temperature or self.temperature
                    }
                )
                content = response.text
            else:
                # For multi-turn, use chat
                chat = self.model.start_chat(history=user_messages[:-1])
                response = await chat.send_message_async(
                    user_messages[-1]["parts"][0],
                    generation_config={
                        "max_output_tokens": max_tokens or self.max_tokens,
                        "temperature": temperature or self.temperature
                    }
                )
                content = response.text

            logger.debug(f"Gemini response: {content[:100]}...")
            return content

        except Exception as e:
            logger.error(f"Google error: {e}")
            raise Exception(f"Google request failed: {e}")

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
