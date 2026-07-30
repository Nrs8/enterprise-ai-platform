from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from app.memory.models import Message
from app.llm.models import LLMResponse


class BaseLLM(ABC):

    @abstractmethod
    async def generate(
        self,
        messages: list[Message],
    ) -> LLMResponse:
        """
        Generate a response from the LLM.
        """
        pass