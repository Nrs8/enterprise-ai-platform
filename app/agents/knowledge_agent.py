"""
Knowledge Agent.

Responsible for knowledge retrieval
and answer generation.
"""


from app.agents.base import BaseAgent

from app.runtime.context import AgentContext

from app.runtime.steps.retrieve import RetrieveStep

from app.runtime.steps.llm import LLMStep





class KnowledgeAgent(BaseAgent):
    """
    Agent responsible for knowledge retrieval
    and answer generation.
    """


    name = "knowledge_agent"


    description = (
        "Handles knowledge retrieval "
        "using RAG and LLM."
    )



    def __init__(

        self,

        retrieve_step: RetrieveStep,

        llm_step: LLMStep,

    ) -> None:


        self.retrieve_step = (
            retrieve_step
        )


        self.llm_step = (
            llm_step
        )



    async def execute(

        self,

        context: AgentContext,

    ) -> AgentContext:
        """
        Execute RAG workflow.

        Flow:

        User Input

            |

            v

        RetrieveStep

            |

            v

        LLMStep

            |

            v

        Response
        """



        #
        # Retrieve knowledge
        #

        await self.retrieve_step.execute(

            context

        )



        #
        # Generate answer
        #

        await self.llm_step.execute(

            context

        )



        #
        # Save final response
        #

        if context.llm_response:

            context.response = (
                context.llm_response.content
            )



        return context