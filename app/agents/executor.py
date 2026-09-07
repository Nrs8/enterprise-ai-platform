"""
Agent execution boundary.

Responsible for executing agents through
the official Agent lifecycle contract.
"""

from __future__ import annotations

import logging

from app.agents.base import BaseAgent
from app.agents.models import AgentResult
from app.runtime.context import AgentContext
from app.runtime.errors import build_error_info


logger = logging.getLogger(
    "app.agent.executor"
)


class AgentExecutor:
    """
    Executes agents through the standard
    Agent execution contract.

    Flow:

        AgentContext
              |
              v
        AgentExecutor
              |
              v
        BaseAgent.execute()
              |
              v
        AgentResult


    AgentExecutor is an execution boundary.

    AgentExecutor does NOT:

    - route agents
    - manage memory
    - manage conversations
    - perform reasoning
    - perform tool calling
    - implement retry policies

    It only provides a safe execution
    boundary for Agent execution.
    """

    async def execute(
        self,
        agent: BaseAgent,
        context: AgentContext,
    ) -> AgentResult:
        """
        Execute an agent safely.

        Calls the official Agent contract:

            BaseAgent.execute()

        Returns:
            AgentResult produced by the agent.

        Unexpected exceptions are converted
        into a failed AgentResult.
        """

        try:
            result = await agent.execute(
                context
            )

            if not isinstance(
                result,
                AgentResult,
            ):
                raise TypeError(
                    "Agent.execute() must return AgentResult"
                )

            return result

        except Exception as exc:
            logger.exception(
                "Agent execution failed: %s",
                agent.name,
            )

            return AgentResult.failure(
                error=build_error_info(exc),
                agent=agent.name,
            )