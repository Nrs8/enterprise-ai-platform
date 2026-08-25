"""
Agent execution wrapper.

Responsible for executing agents
with common runtime policies.
"""


from __future__ import annotations


import logging


from app.agents.base import BaseAgent
from app.agents.models import AgentResult

from app.runtime.context import AgentContext



logger = logging.getLogger(
    "app.agent.executor"
)





class AgentExecutor:
    """
    Executes agents.

    Centralizes agent lifecycle handling.

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


    AgentExecutor does NOT:

    - route agents
    - manage memory
    - manage conversations
    - perform reasoning

    It only provides a safe
    execution boundary.
    """



    async def execute(
        self,
        agent: BaseAgent,
        context: AgentContext,
    ) -> AgentResult:
        """
        Execute agent safely.

        Calls the official Agent contract:

            BaseAgent.execute()
        """

        try:

            result = await agent.execute(
                context
            )


            return result



        except Exception as exc:

            logger.exception(
                "Agent execution failed"
            )


            return AgentResult(

                success=False,

                agent=agent.name,

                error=str(exc),

            )