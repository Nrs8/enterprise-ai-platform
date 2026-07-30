"""
LLM gateway abstraction layer.
"""

from app.llm.qwen import QwenLLM
from app.memory.models import Message
from app.llm.models import LLMResponse

class LLMGateway:
    """
    Provides a unified interface for LLM communication.
    """

    def __init__(self) -> None:
        """
        Initialize LLM gateway.
        """

        self._provider = QwenLLM()

    async def generate(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
    ) -> LLMResponse:
        """
        Generate response from LLM provider.

        Args:
            messages:
                Conversation history.

        Returns:
            Assistant response.
        """

        return await self._provider.generate(
            messages=messages,
            tools=tools,
        )