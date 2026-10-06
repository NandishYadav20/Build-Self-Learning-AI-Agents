"""Base Agent class implementing core LLM patterns"""

from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel, Field
import json
from openai import AsyncOpenAI, OpenAI
import asyncio

from ..utils.config import get_settings
from ..utils.logger import logger


class Message(BaseModel):
    """Message data model"""
    role: str  # system, user, assistant
    content: str


class ToolDefinition(BaseModel):
    """Tool/Function definition for LLM"""
    type: str = "function"
    function: Dict[str, Any]


class BaseAgent(ABC):
    """
    Base Agent class with core LLM patterns:
    - Prompt chaining
    - Routing
    - Tool use
    - Structured output
    """

    def __init__(
        self,
        name: str,
        description: str,
        system_prompt: str,
        tools: Optional[List[ToolDefinition]] = None,
    ):
        """
        Initialize base agent

        Args:
            name: Agent name
            description: Agent description
            system_prompt: System prompt for the agent
            tools: Optional list of available tools/functions
        """
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.conversation_history: List[Message] = []
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.async_client = AsyncOpenAI(api_key=self.settings.openai_api_key)

    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append(Message(role=role, content=content))

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history as dicts for API"""
        return [{"role": msg.role, "content": msg.content} for msg in self.conversation_history]

    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info(f"Agent {self.name} conversation history cleared")

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Build messages list with system prompt"""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.get_conversation_history())
        if user_input:
            messages.append({"role": "user", "content": user_input})
        return messages

    def call_llm(
        self,
        user_input: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Any] = None,
    ) -> str:
        """
        Make a basic LLM API call

        Args:
            user_input: User input text
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            response_format: Response format specification (for structured output)

        Returns:
            LLM response text
        """
        messages = self._build_messages(user_input)

        kwargs = {
            "model": self.settings.openai_model,
            "messages": messages,
            "temperature": temperature or self.settings.openai_temperature,
            "max_tokens": max_tokens or self.settings.openai_max_tokens,
        }

        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content

            # Add to history
            self.add_message("user", user_input)
            self.add_message("assistant", content)

            logger.info(f"Agent {self.name} received response")
            return content

        except Exception as e:
            logger.error(f"Error in LLM call: {str(e)}")
            raise

    def call_llm_with_tools(
        self,
        user_input: str,
        tool_choice: str = "auto",
    ) -> Dict[str, Any]:
        """
        Make LLM call with tools available

        Args:
            user_input: User input text
            tool_choice: Tool choice strategy (auto, required, none)

        Returns:
            Response with potential tool calls
        """
        messages = self._build_messages(user_input)

        kwargs = {
            "model": self.settings.openai_model,
            "messages": messages,
            "tools": [tool.model_dump() for tool in self.tools] if self.tools else None,
            "tool_choice": tool_choice,
            "temperature": self.settings.openai_temperature,
            "max_tokens": self.settings.openai_max_tokens,
        }

        # Remove tools if empty
        if not kwargs["tools"]:
            del kwargs["tools"]
            del kwargs["tool_choice"]

        try:
            response = self.client.chat.completions.create(**kwargs)

            # Add to history
            self.add_message("user", user_input)
            self.add_message("assistant", response.choices[0].message.content or "")

            return {
                "content": response.choices[0].message.content,
                "tool_calls": getattr(response.choices[0].message, "tool_calls", None),
                "finish_reason": response.choices[0].finish_reason,
            }

        except Exception as e:
            logger.error(f"Error in LLM tool call: {str(e)}")
            raise

    async def call_llm_async(
        self,
        user_input: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Async version of LLM call"""
        messages = self._build_messages(user_input)

        kwargs = {
            "model": self.settings.openai_model,
            "messages": messages,
            "temperature": temperature or self.settings.openai_temperature,
            "max_tokens": max_tokens or self.settings.openai_max_tokens,
        }

        try:
            response = await self.async_client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content

            self.add_message("user", user_input)
            self.add_message("assistant", content)

            return content

        except Exception as e:
            logger.error(f"Error in async LLM call: {str(e)}")
            raise

    @abstractmethod
    async def process(self, input_data: str) -> str:
        """Process input - implemented by subclasses"""
        pass
