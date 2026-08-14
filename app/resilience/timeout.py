import asyncio
from typing import Callable, Any

from app.resilience.exceptions import LLMError


async def timeout(
    func: Callable,
    *args,
    seconds: float = 90,
    **kwargs,
) -> Any:

    try:

        return await asyncio.wait_for(
            func(*args, **kwargs),
            timeout=seconds,
        )

    except asyncio.TimeoutError as e:

        raise LLMError(
            f"LLM request timeout after {seconds}s"
        ) from e