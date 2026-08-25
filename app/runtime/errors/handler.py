"""
Runtime error handler.

Converts exceptions into
structured runtime error information.

This module MUST NOT depend on
Agent models or Runtime classes.

Layer:

Exception
    |
    v
RuntimeErrorInfo
"""

from __future__ import annotations


from app.runtime.errors.models import (
    RuntimeErrorInfo,
    ErrorCategory,
)


from app.runtime.errors.exceptions import (
    RuntimeErrorBase,
)



def build_error_info(
    exc: Exception,
) -> RuntimeErrorInfo:
    """
    Convert exception into structured runtime error.

    Expected runtime exceptions keep their
    original category and retry information.

    Unexpected exceptions are converted into
    INTERNAL errors.
    """


    if isinstance(
        exc,
        RuntimeErrorBase,
    ):

        return RuntimeErrorInfo(

            code=exc.code,

            message=exc.message,

            category=exc.category,

            retryable=exc.retryable,

        )



    return RuntimeErrorInfo(

        code="internal_error",

        message=str(exc),

        category=(
            ErrorCategory.INTERNAL
        ),

        retryable=False,

    )