import asyncio
import logging
from typing import Callable, Any

from app.config.settings import settings
from app.resilience.timeout import timeout

logger = logging.getLogger(__name__)


async def retry(
    func: Callable,
    *args,
    delay: float = 1.0,
    **kwargs,
) -> Any:
    """
    Async retry wrapper.
    """

    last_exception = None

    retries = settings.retry_count

    for attempt in range(1, retries + 1):

        try:

            return await timeout(
                func,
                *args,
                **kwargs,
            )


        except Exception as e:

            last_exception = e

            logger.warning(
                "Retry attempt %s/%s failed: %s",
                attempt,
                retries,
                e,
            )

            if attempt < retries:
                await asyncio.sleep(delay)


    logger.error(
        "All retry attempts failed: %s",
        retries,
    )

    raise last_exception