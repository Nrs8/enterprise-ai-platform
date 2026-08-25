"""
Base agent abstraction.

Defines common interface
for all enterprise agents.
"""


from __future__ import annotations


from abc import ABC, abstractmethod

import logging


from app.agents.models import AgentResult
from app.runtime.context import AgentContext



logger = logging.getLogger(
    "app.agents.base"
)





class BaseAgent(ABC):
    """
    Base class for all enterprise agents.

    Agent contract:

        AgentContext
              |
              v
        execute()
              |
              v
        AgentResult


    All concrete agents must implement:

        execute(context)

    Agents should only handle
    domain-specific execution logic.
    """



    name: str = "base_agent"





    async def run(
        self,
        context: AgentContext,
    ) -> AgentResult:
        """
        Backward compatibility wrapper.

        Deprecated:

            Use execute() directly.

        This method exists only for
        legacy workflow components
        that still call run().
        """


        logger.debug(

            "Agent.run() forwarding to execute(): %s",

            self.name,

        )


        return await self.execute(
            context
        )







    @abstractmethod
    async def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:
        """
        Execute agent behavior.


        Parameters
        ----------
        context:
            Runtime execution context.


        Returns
        -------
        AgentResult
            Standardized execution result.


        Implementations should:

        - perform agent-specific reasoning
        - call required runtime components
        - return AgentResult


        Implementations should NOT:

        - persist memory
        - route agents
        - manage conversations
        - control runtime lifecycle
        """


        raise NotImplementedError