"""
LLM execution step.

Responsible for:

1. Building prompt messages
2. Calling LLM Gateway
3. Saving LLM response into AgentContext
"""

import logging

from app.runtime.steps.base import AgentStep
from app.llm.models import LLMResponse


logger = logging.getLogger(__name__)


class LLMStep(AgentStep):
    """
    Responsible for prompt construction
    and LLM generation.
    """

    def __init__(
        self,
        llm_gateway,
        prompt_builder,
        tool_registry,
    ) -> None:
        """
        Initialize LLM step.
        """

        self._llm_gateway = llm_gateway

        self._prompt_builder = prompt_builder

        self._tool_registry = tool_registry


    async def execute(
        self,
        context,
    ) -> LLMResponse:
        """
        Execute LLM generation.
        """

        #
        # Build messages
        #

        if not context.messages:

            context.messages = (
                self._prompt_builder.build(

                    history=
                        context.session.messages,

                    user_message=
                        context.input,

                    knowledge_context=
                        context.knowledge_context,

                )
            )


        logger.info(
            "Calling LLM model=%s",
            context.model,
        )


        #
        # Call LLM
        #

        response = await (
            self._llm_gateway.generate(

                messages=
                    context.messages,


                tools=
                    self._tool_registry.get_schemas(),


                model=
                    context.model,


                session_id=
                    context.session_id,


                user_id=
                    context.user_id,


                tenant_id=
                    context.tenant_id,

            )
        )


        #
        # Safety check
        #

        if response is None:

            raise RuntimeError(
                "LLMGateway returned None"
            )


        #
        # Store response
        #

        context.llm_response = response


        logger.info(
            "LLM completed. tool_calls=%s",
            response.tool_calls,
        )


        return response