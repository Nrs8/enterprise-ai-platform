"""
Fake LLM provider for testing.
"""

from app.llm.models import (
    LLMResponse,
    TokenUsage,
)

from app.llm.providers.base import BaseLLM



class FakeLLM(BaseLLM):
    """
    Fake provider used for testing
    LLM abstraction.
    """


    async def generate(
        self,
        messages,
        tools=None,
    ) -> LLMResponse:

        return LLMResponse(
            content="fake response",

            model="fake-model",

            provider="fake",

            usage=TokenUsage(
                input_tokens=10,
                output_tokens=5,
            ),
        )