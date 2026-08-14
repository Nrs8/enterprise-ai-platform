"""
Supervisor agent.

Responsible for routing user requests
to specialized agents.
"""

import logging

from app.agents.base import BaseAgent
from app.agents.models import AgentDecision
from app.agents.registry import AgentRegistry
from app.runtime.context import AgentContext


logger = logging.getLogger(__name__)


class SupervisorAgent(BaseAgent):
    """
    Agent responsible for routing requests
    to specialized agents.
    """

    name = "supervisor"

    description = (
        "Routes requests to appropriate agents."
    )


    def __init__(
        self,
        registry: AgentRegistry,
        tracer,
    ) -> None:
        """
        Initialize supervisor.

        Args:
            registry:
                Agent registry.

            tracer:
                Observability tracer.
        """

        self.registry = registry

        self.tracer = tracer



    async def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute routing decision
        and delegate execution.
        """


        decision = self._decide(
            context.input
        )


        self._record_decision(
            context,
            decision,
        )


        agent = self.registry.get(
            decision.agent_name
        )


        logger.info(
            "Supervisor selected agent=%s reason=%s confidence=%.2f",
            decision.agent_name,
            decision.reason,
            decision.confidence,
        )


        return await agent.execute(
            context
        )



    def _decide(
        self,
        message: str,
    ) -> AgentDecision:
        """
        Decide target agent.

        Current:
            Rule based routing.

        Future:
            Hybrid rule + LLM router.
        """


        keywords = [

            "document",

            "policy",

            "knowledge",

            "what is",

            "explain",

        ]


        lower = message.lower()



        for keyword in keywords:

            if keyword in lower:

                return AgentDecision(

                    agent_name=(
                        "knowledge_agent"
                    ),

                    reason=(
                        f"matched keyword: {keyword}"
                    ),

                    confidence=0.9,

                )



        return AgentDecision(

            agent_name=(
                "tool_agent"
            ),

            reason=(
                "default tool agent routing"
            ),

            confidence=0.7,

        )



    def _record_decision(
        self,
        context: AgentContext,
        decision: AgentDecision,
    ) -> None:
        """
        Record supervisor decision.

        Keeps routing visibility for
        production debugging.
        """


        if self.tracer is None:

            return



        try:

            self.tracer.add_event(

                "supervisor_decision",

                {

                    "session_id":
                        context.session_id,

                    "input":
                        context.input,

                    "agent":
                        decision.agent_name,

                    "reason":
                        decision.reason,

                    "confidence":
                        decision.confidence,

                },

            )


        except Exception:

            logger.exception(
                "Failed to record supervisor decision"
            )