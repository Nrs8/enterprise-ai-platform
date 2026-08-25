"""
LLM domain models.
"""

from dataclasses import dataclass, field

from typing import Any



@dataclass
class Message:
    """
    Message format used by LLM runtime.

    Supports:
    - normal conversation
    - assistant tool calls
    - tool responses
    """

    role: str

    content: str | None = None

    tool_calls: list[Any] = field(
        default_factory=list
    )

    tool_call_id: str | None = None



@dataclass
class TokenUsage:
    """
    Token consumption information.
    """

    input_tokens: int = 0

    output_tokens: int = 0


    @property
    def total_tokens(self) -> int:
        return (
            self.input_tokens
            +
            self.output_tokens
        )



@dataclass
class ToolCall:
    """
    Represents a tool call requested by LLM.
    """

    id: str

    name: str

    arguments: dict[str, Any]



@dataclass
class LLMResponse:
    """
    Normalized response returned by LLM.
    """

    content: str | None = None

    tool_calls: list[ToolCall] = field(
        default_factory=list
    )

    model: str | None = None

    provider: str | None = None

    usage: TokenUsage | None = None



@dataclass
class ToolResult:
    """
    Represents tool execution result.
    """

    success: bool

    content: str | None = None

    error: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )