"""
Supervisor agent.

Responsible only for routing decisions.

Supervisor does NOT execute agents.

Flow:

AgentRuntime
      |
      v
SupervisorAgent
      |
      v
AgentDecision
      |
      v
AgentRegistry
      |
      v
Specialized Agent
"""


from __future__ import annotations


import logging


from app.agents.models import AgentDecision

from app.runtime.context import AgentContext



logger = logging.getLogger(
    __name__
)





class SupervisorAgent:
    """
    Responsible for agent routing.

    Responsibilities:

    - Analyze user request
    - Select target agent
    - Produce AgentDecision


    Supervisor does NOT:

    - execute agents
    - call LLM
    - run tools
    - modify memory
    """



    name = "supervisor"



    description = (
        "Routes requests to appropriate agents."
    )





    def __init__(
        self,
        tracer=None,
    ) -> None:
        """
        Initialize supervisor.
        """

        self.tracer = tracer







    async def decide(
        self,
        context: AgentContext,
    ) -> AgentDecision:
        """
        Decide which agent should handle request.

        Runtime executes
        the selected agent.
        """



        decision = self._decide(
            context.input
        )



        self._record_decision(
            context,
            decision,
        )



        logger.info(
            "Supervisor selected agent=%s "
            "reason=%s confidence=%.2f",
            decision.agent_name,
            decision.reason,
            decision.confidence,
        )



        return decision







    def _decide(
        self,
        message: str,
    ) -> AgentDecision:
        """
        Routing logic.

        Current:

            Rule based routing


        Future:

            Hybrid:

                Rule
                  +
                LLM Router
        """



        lower = message.lower()



        #
        # Customer service routing
        #

        customer_keywords = [

            "ticket",

            "complaint",

            "problem",

            "issue",

            "support",

            "refund",

            "order",

            "customer",

            "account",

        ]



        for keyword in customer_keywords:


            if keyword in lower:


                return AgentDecision(

                    agent_name=
                        "customer_service_agent",


                    reason=
                        f"matched customer keyword: {keyword}",


                    confidence=0.85,

                )







        #
        # Knowledge routing
        #

        knowledge_keywords = [

            "document",

            "policy",

            "knowledge",

            "what is",

            "explain",

        ]



        for keyword in knowledge_keywords:


            if keyword in lower:


                return AgentDecision(

                    agent_name=
                        "knowledge_agent",


                    reason=
                        f"matched keyword: {keyword}",


                    confidence=0.9,

                )







        #
        # Default tool routing
        #

        return AgentDecision(

            agent_name=
                "tool_agent",


            reason=
                "default tool agent routing",


            confidence=0.7,

        )









    def _record_decision(
        self,
        context: AgentContext,
        decision: AgentDecision,
    ) -> None:
        """
        Record routing decision.
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