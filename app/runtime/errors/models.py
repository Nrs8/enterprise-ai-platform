"""
Runtime error models.

Defines structured errors returned
from AgentRuntime execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ErrorCategory(str, Enum):
    """
    Runtime error categories.
    """

    VALIDATION = "validation"

    AUTHORIZATION = "authorization"

    TOOL_FAILURE = "tool_failure"

    LLM_FAILURE = "llm_failure"

    MEMORY_FAILURE = "memory_failure"

    MCP_FAILURE = "mcp_failure"

    INTERNAL = "internal"


@dataclass
class RuntimeErrorInfo:
    """
    Serializable runtime error information.
    """

    code: str

    message: str

    category: ErrorCategory

    retryable: bool = False