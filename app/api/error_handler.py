"""
FastAPI error handling.

Translates runtime exceptions into
stable HTTP error responses.
"""

from __future__ import annotations


from fastapi import (
    Request,
)

from fastapi.responses import (
    JSONResponse,
)


from app.runtime.errors import (
    ErrorCategory,
    RuntimeErrorBase,
    build_error_info,
)



def _status_code_for_category(
    category: ErrorCategory,
) -> int:
    """
    Map runtime error categories to HTTP status codes.
    """

    mapping = {

        ErrorCategory.VALIDATION: 400,

        ErrorCategory.AUTHORIZATION: 403,

        ErrorCategory.TOOL_FAILURE: 502,

        ErrorCategory.LLM_FAILURE: 502,

        ErrorCategory.MEMORY_FAILURE: 500,

        ErrorCategory.MCP_FAILURE: 502,

        ErrorCategory.INTERNAL: 500,

    }


    return mapping.get(
        category,
        500,
    )



async def runtime_exception_handler(
    request: Request,
    exc: RuntimeErrorBase,
) -> JSONResponse:
    """
    Convert a runtime exception into an HTTP response.
    """

    error = build_error_info(
        exc
    )


    status_code = (
        _status_code_for_category(
            error.category
        )
    )


    return JSONResponse(

        status_code=status_code,

        content={
            "error": {
                "code": error.code,
                "message": error.message,
                "category": (
                    error.category.value
                ),
                "retryable": (
                    error.retryable
                ),
            }
        },
    )