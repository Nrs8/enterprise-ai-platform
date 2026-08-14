"""
Agent domain models.

Contains shared models used by
multi-agent orchestration.
"""

from dataclasses import dataclass


@dataclass
class AgentDecision:
    """
    Represents a supervisor routing decision.

    Attributes:
        agent_name:
            Target agent selected.

        reason:
            Explanation for routing decision.

        confidence:
            Confidence score between 0.0 and 1.0.
    """

    agent_name: str

    reason: str

    confidence: float