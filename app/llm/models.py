"""
LLM domain models.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TokenUsage:
    """
    Token consumption information returned by LLM provider.
    """

    input_tokens: int = 0

    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


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

    model: str | None = None

    provider: str | None = None

    usage: TokenUsage | None = None


@dataclass
class ToolResult:
    """
    Represents the result of a tool execution.
    """

    success: bool

    content: str | None = None

    error: str | None = None