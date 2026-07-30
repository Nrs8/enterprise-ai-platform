"""
Qwen LLM provider implementation.
"""

import json

from openai import AsyncOpenAI

from app.config import settings
from app.llm.base import BaseLLM
from app.llm.models import LLMResponse, ToolCall
from app.memory.models import Message


class QwenLLM(BaseLLM):
    """
    Qwen model provider.
    """

    def __init__(self) -> None:
        """
        Initialize Qwen client.
        """

        self.client = AsyncOpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
        )

        self.model = settings.model

    async def generate(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
    ) -> LLMResponse:
        """
        Generate response using Qwen.

        Args:
            messages:
                Conversation history.

            tools:
                Available tools for the LLM.

        Returns:
            Normalized LLM response.
        """

        qwen_messages = []

        for message in messages:
            qwen_message = {
                "role": message.role,
                "content": message.content,
            }

            if message.tool_calls:
                qwen_message["tool_calls"] = [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.name,
                            "arguments": json.dumps(
                                tool_call.arguments
                            ),
                        },
                    }
                    for tool_call in message.tool_calls
                ]

            if message.tool_call_id:
                qwen_message["tool_call_id"] = message.tool_call_id

            qwen_messages.append(qwen_message)

        request_kwargs = {
            "model": self.model,
            "messages": qwen_messages,
        }

        if tools:
            request_kwargs["tools"] = tools

        response = await self.client.chat.completions.create(
            **request_kwargs
        )

        message = response.choices[0].message

        tool_calls = []

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=tool_call.id,
                        name=tool_call.function.name,
                        arguments=json.loads(
                            tool_call.function.arguments
                        ),
                    )
                )

        return LLMResponse(
            content=message.content,
            tool_calls=tool_calls or None,
        )