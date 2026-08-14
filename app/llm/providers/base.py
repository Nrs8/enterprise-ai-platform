"""
Base LLM provider interface.
"""

from abc import ABC, abstractmethod

from app.llm.models import LLMResponse


class BaseLLM(ABC):
    """
    Abstract interface for all LLM providers.
    """

    @abstractmethod
    async def generate(
        self,
        messages,
        tools=None,
    ) -> LLMResponse:
        """
        Generate response from LLM.

        Args:
            messages:
                Conversation messages.

            tools:
                Available tool schemas.

        Returns:
            Unified LLMResponse.
        """
        pass