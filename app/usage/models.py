"""
Usage tracking domain models.
"""

from dataclasses import dataclass


@dataclass
class UsageRecord:
    """
    Represents one LLM usage event.
    """

    request_id: str

    session_id: str | None

    provider: str

    model: str

    input_tokens: int

    output_tokens: int

    latency_ms: float

    cost: float = 0.0

    user_id: str | None = None

    tenant_id: str | None = None

    @property
    def total_tokens(self) -> int:
        """
        Return total token usage.
        """

        return self.input_tokens + self.output_tokens