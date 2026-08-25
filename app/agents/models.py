"""
Agent data models.

Shared models used by:

- SupervisorAgent
- KnowledgeAgent
- ToolAgent
- Workflow Engine
"""

from __future__ import annotations


from dataclasses import dataclass, field


from typing import Any, Dict, Optional, List


from app.runtime.errors import (
    RuntimeErrorInfo,
)



# ============================================================
# Agent Decision
# ============================================================


@dataclass
class AgentDecision:
    """
    Represents a routing decision.

    Created by SupervisorAgent.
    """

    agent_name: str

    reason: Optional[str] = None

    confidence: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Agent Result
# ============================================================


@dataclass
class AgentResult:
    """
    Standard result returned by agents.

    All agents MUST return this object.

    Examples:

    ToolAgent
    KnowledgeAgent
    WorkflowExecutor

    The runtime uses this object
    as the boundary between agent execution
    and upper application layers.
    """


    success: bool = True


    response: Optional[str] = None


    agent: Optional[str] = None


    error: Optional[RuntimeErrorInfo] = None


    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



    @classmethod
    def failure(
        cls,
        error: RuntimeErrorInfo,
        agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentResult":
        """
        Create failed agent result.
        """

        return cls(
            success=False,
            response=None,
            agent=agent,
            error=error,
            metadata=metadata or {},
        )


    @classmethod
    def success_result(
        cls,
        response: str,
        agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentResult":
        """
        Create successful agent result.
        """

        return cls(
            success=True,
            response=response,
            agent=agent,
            metadata=metadata or {},
        )



# ============================================================
# Agent Metadata
# ============================================================


@dataclass
class AgentMetadata:
    """
    Describes agent capability.
    """


    name: str


    description: str


    capabilities: List[str] = field(
        default_factory=list
    )



__all__ = [

    "AgentDecision",

    "AgentResult",

    "AgentMetadata",

]