import asyncio
import logging
from typing import Callable, Any

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)

from app.config.settings import settings
from app.resilience.exceptions import LLMError
from app.resilience.timeout import timeout


logger = logging.getLogger(__name__)


RETRYABLE_EXCEPTIONS = (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
    LLMError,
)


async def retry(
    func: Callable,
    *args,
    delay: float = 1.0,
    **kwargs,
) -> Any:
    """
    Async retry wrapper.

    Retries only transient LLM failures such as
    connection errors, timeouts, rate limits, and
    server-side errors.
    """

    attempts = max(
        1,
        settings.retry_count,
    )

    last_exception = None

    for attempt in range(1, attempts + 1):

        try:
            return await timeout(
                func,
                *args,
                seconds=settings.llm_timeout,
                **kwargs,
            )

        except RETRYABLE_EXCEPTIONS as exc:

            last_exception = exc

            logger.warning(
                "Retryable LLM failure "
                "attempt %s/%s: %s: %s",
                attempt,
                attempts,
                type(exc).__name__,
                exc,
            )

            if attempt < attempts:
                await asyncio.sleep(delay)

        except Exception:
            raise

    logger.error(
        "All LLM retry attempts failed: %s",
        attempts,
    )

    raise last_exception