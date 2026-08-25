"""
Runtime exception hierarchy.
"""

from __future__ import annotations

from app.runtime.errors.models import (
    ErrorCategory,
)


class RuntimeErrorBase(Exception):
    """
    Base runtime exception.

    All expected runtime failures
    should inherit from this class.
    """

    category: ErrorCategory = (
        ErrorCategory.INTERNAL
    )

    code: str = "runtime_error"

    def __init__(
        self,
        message: str,
        retryable: bool = False,
    ) -> None:

        self.message = message

        self.retryable = retryable

        super().__init__(message)


class ToolExecutionError(RuntimeErrorBase):
    """
    Tool execution failure.
    """

    category = ErrorCategory.TOOL_FAILURE

    code = "tool_execution_failed"


class LLMExecutionError(RuntimeErrorBase):
    """
    LLM provider failure.
    """

    category = ErrorCategory.LLM_FAILURE

    code = "llm_execution_failed"


class MemoryError(RuntimeErrorBase):
    """
    Memory subsystem failure.
    """

    category = ErrorCategory.MEMORY_FAILURE

    code = "memory_failure"


class MCPExecutionError(RuntimeErrorBase):
    """
    MCP subsystem failure.
    """

    category = ErrorCategory.MCP_FAILURE

    code = "mcp_execution_failed"