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

        Returns:

            AgentDecision

        Runtime will execute
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

                    agent_name=
                        "knowledge_agent",


                    reason=
                        f"matched keyword: {keyword}",


                    confidence=0.9,

                )





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