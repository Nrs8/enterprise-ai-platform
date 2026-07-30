"""
LLM domain models.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCall:
    """
    Represents a tool call requested by the LLM.
    """

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    """
    Normalized response returned by the LLM.
    """

    content: str | None = None
    tool_calls: list[ToolCall] | None = None

@dataclass
class ToolResult:
    """
    Represents the result of a tool execution.
    """

    success: bool
    content: str | None = None
    error: str | None = None