"""
Tool execution agent.

Responsible for executing
tool-based reasoning workflow.
"""

from __future__ import annotations

import logging

from app.agents.base import BaseAgent
from app.agents.models import AgentResult
from app.runtime.context import AgentContext

logger = logging.getLogger(
    "app.agents.tool_agent"
)


class ToolAgent(BaseAgent):
    """
    Agent responsible for
    tool-based tasks.

    Flow:

        AgentContext
             |
             v
        ToolAgent.execute()
             |
             v
        ToolCallingExecutor
             |
             v
        LLM
             |
             v
        Tool execution
             |
             v
        AgentResult

    ToolAgent owns the Agent lifecycle entry point.

    ToolCallingExecutor owns the
    LLM/tool calling loop.

    Unexpected execution failures are
    propagated to AgentExecutor, which
    provides the common execution boundary.
    """

    name = "tool_agent"

    def __init__(
        self,
        tool_calling_executor,
    ) -> None:
        self._tool_calling_executor = (
            tool_calling_executor
        )

    async def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:
        """
        Execute the tool agent.

        Delegates the reasoning loop to
        ToolCallingExecutor.

        Unexpected exceptions are propagated
        to the AgentExecutor boundary.
        """

        logger.info(
            "ToolAgent executing"
        )

        await self._tool_calling_executor.execute(
            context
        )

        return AgentResult(
            response=context.response or "",
            success=True,
            agent=self.name,
            metadata={
                "type": "tool_execution"
            },
        )
