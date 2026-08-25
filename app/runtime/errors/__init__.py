"""
Runtime error package.

Provides:

- Error categories
- Structured error models
- Runtime exceptions
- Exception conversion helpers
"""

from app.runtime.errors.models import (
    ErrorCategory,
    RuntimeErrorInfo,
)


from app.runtime.errors.exceptions import (
    RuntimeErrorBase,
    ToolExecutionError,
    LLMExecutionError,
    MemoryError,
    MCPExecutionError,
)


from app.runtime.errors.handler import (
    build_error_info,
)



__all__ = [

    "ErrorCategory",

    "RuntimeErrorInfo",

    "RuntimeErrorBase",

    "ToolExecutionError",

    "LLMExecutionError",

    "MemoryError",

    "MCPExecutionError",

    "build_error_info",

]