"""
LLM gateway abstraction layer.
"""

import logging
import time
from uuid import uuid4

from app.memory.models import Message
from app.observability.metrics import metrics

from app.llm.models import LLMResponse
from app.llm.router import ModelRouter

from app.resilience.retry import retry

from app.usage.models import UsageRecord
from app.usage.tracker import UsageTracker


logger = logging.getLogger(__name__)


class LLMGateway:
    """
    Provides a unified interface for LLM communication.
    """

    def __init__(
        self,
        router: ModelRouter,
        usage_tracker: UsageTracker,
    ) -> None:
        """
        Initialize LLM gateway.
        """

        self._router = router
        self._usage_tracker = usage_tracker

    async def generate(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        model: str = "qwen",
        session_id: str | None = None,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ) -> LLMResponse:
        """
        Generate response from LLM provider.

        Args:
            messages:
                Conversation messages.

            tools:
                Available tools.

            model:
                Provider routing key.

            session_id:
                Conversation session identifier.

            user_id:
                User identity for governance tracking.

            tenant_id:
                Tenant identity for governance tracking.

        Returns:
            Unified LLMResponse.
        """

        metrics.increment(
            "llm_calls"
        )

        provider = self._router.get_provider(
            model
        )

        logger.info(
            "Selected LLM provider: %s",
            provider.__class__.__name__,
        )

        start_time = time.perf_counter()

        try:

            response: LLMResponse = await retry(
                provider.generate,
                messages=messages,
                tools=tools,
            )

            latency_ms = (
                time.perf_counter()
                - start_time
            ) * 1000


            logger.info(
                "LLM response model=%s provider=%s",
                response.model,
                response.provider,
            )


            if response.usage:

                logger.info(
                    "Token usage input=%s output=%s",
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                )


                usage_record = UsageRecord(
                    request_id=str(uuid4()),

                    session_id=session_id,

                    provider=response.provider
                    or "unknown",

                    model=response.model
                    or "unknown",

                    input_tokens=(
                        response.usage.input_tokens
                    ),

                    output_tokens=(
                        response.usage.output_tokens
                    ),

                    latency_ms=latency_ms,

                    cost=0.0,

                    user_id=user_id,

                    tenant_id=tenant_id,
                )


                self._usage_tracker.record(
                    usage_record
                )


            return response


        finally:

            latency = (
                time.perf_counter()
                - start_time
            )


            logger.info(
                "LLM latency: %.3fs",
                latency,
            )