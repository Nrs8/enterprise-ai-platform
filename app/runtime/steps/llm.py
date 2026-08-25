"""
LLM execution step.

Responsible for:

1. Building prompt messages
2. Calling LLM Gateway
3. Saving LLM response into AgentContext
"""


from __future__ import annotations


import logging


from app.runtime.steps.base import (
    AgentStep,
)


from app.llm.models import (
    LLMResponse,
)



logger = logging.getLogger(
    __name__
)








class LLMStep(AgentStep):
    """
    Responsible for LLM generation.


    Responsibilities:

    - Build prompt
    - Call LLM Gateway
    - Store LLM response


    Does NOT:

    - Manage memory
    - Execute tools
    - Route agents
    """







    def __init__(

        self,

        llm_gateway,

        prompt_builder,

        tool_registry,

    ) -> None:


        self._llm_gateway = (
            llm_gateway
        )


        self._prompt_builder = (
            prompt_builder
        )


        self._tool_registry = (
            tool_registry
        )









    async def execute(

        self,

        context,

    ) -> LLMResponse:
        """
        Execute LLM generation.


        Flow:


        AgentContext

             |

             v


        PromptBuilder


             |

             v


        LLM Messages


             |

             v


        LLM Gateway


             |

             v


        LLMResponse

        """







        #
        # Build prompt messages
        #
        # Only build once.
        #
        # Tool calling loop will
        # append messages later.
        #

        if not context.messages:


            context.messages = (

                self._prompt_builder.build(

                    context

                )

            )








        logger.info(

            "LLM messages count=%s",

            len(

                context.messages

            ),

        )








        for message in context.messages:


            logger.debug(

                "LLM message role=%s content=%s",

                message.role,

                (

                    message.content[:100]

                    if message.content

                    else ""

                ),

            )









        #
        # Generate response
        #

        response = await (

            self._llm_gateway.generate(

                messages=(

                    context.messages

                ),


                tools=(

                    self._tool_registry

                    .get_schemas()

                ),


                model=(

                    context.model

                ),


                session_id=(

                    context.session_id

                ),


                user_id=(

                    context.user_id

                ),


                tenant_id=(

                    context.tenant_id

                ),

            )

        )








        if response is None:


            raise RuntimeError(

                "LLMGateway returned None"

            )









        #
        # Save LLM response
        #

        context.set_llm_response(

            response

        )









        logger.info(

            "LLM completed. tool_calls=%s",

            response.tool_calls,

        )








        return response