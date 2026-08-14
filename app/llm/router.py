"""
LLM provider router.
"""

import logging

from app.llm.providers.base import BaseLLM


logger = logging.getLogger(__name__)


class ModelRouter:
    """
    Resolve model name to LLM provider.
    """


    def __init__(
        self,
        providers: dict[str, BaseLLM],
    ):
        self.providers = providers


    def get_provider(
        self,
        model_name: str,
    ) -> BaseLLM:
        """
        Get LLM provider by name.
        """

        provider = self.providers.get(
            model_name
        )


        if provider is None:

            raise ValueError(
                f"Unknown model: {model_name}"
            )


        logger.info(
            "Selected provider: %s",
            model_name,
        )


        return provider