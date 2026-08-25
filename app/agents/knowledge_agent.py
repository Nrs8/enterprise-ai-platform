"""
Knowledge Agent.

Responsible for retrieval
augmented generation.
"""


from __future__ import annotations


import logging


from app.agents.base import BaseAgent
from app.agents.models import AgentResult

from app.runtime.context import AgentContext



logger = logging.getLogger(
    "app.agents.knowledge_agent"
)





class KnowledgeAgent(BaseAgent):
    """
    Agent responsible for
    knowledge retrieval.


    Flow:

        AgentContext
             |
             v
        RetrieveStep
             |
             v
        LLMStep
             |
             v
        AgentResult
    """



    name = "knowledge_agent"





    def __init__(
        self,
        retrieve_step,
        llm_step,
    ) -> None:


        self._retrieve_step = (
            retrieve_step
        )


        self._llm_step = (
            llm_step
        )





    async def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:
        """
        Execute knowledge workflow.
        """


        logger.info(
            "KnowledgeAgent executing"
        )


        try:


            #
            # Retrieve documents
            #

            await (
                self._retrieve_step
                .execute(
                    context
                )
            )



            #
            # Generate answer
            #

            response = await (
                self._llm_step
                .execute(
                    context
                )
            )


            content = (
                response.content
                or ""
            )



            context.set_response(
                content
            )



            return AgentResult(

                response=content,

                success=True,

                agent=self.name,

                metadata={

                    "type":
                    "knowledge_retrieval",

                },

            )



        except Exception as exc:


            logger.exception(
                "KnowledgeAgent failed"
            )


            return AgentResult(

                response=(
                    "Knowledge retrieval failed"
                ),

                success=False,

                agent=self.name,

                error=str(exc),

            )