"""
Agent execution loop.

Responsible for:
    LLM -> Tool -> LLM iteration
"""

import logging

from app.memory.models import Message


logger = logging.getLogger("app.runtime.loop")



class AgentLoop:
    """
    Controls iterative agent execution.

    Flow:

        LLMStep
           |
           v
       Tool calls?
          |
      yes | no
          |
          v
       ToolStep
          |
          v
       LLMStep again

    """

    def __init__(
        self,
        llm_step,
        tool_step,
        tracer,
        max_iterations: int = 10,
    ):

        self._llm_step = llm_step

        self._tool_step = tool_step

        self._tracer = tracer

        self._max_iterations = max_iterations



    async def run(
        self,
        context,
    ) -> str:
        """
        Execute agent reasoning loop.

        Args:
            context:
                AgentContext

        Returns:
            Final assistant response.
        """

        messages = context.messages

        trace = context.trace



        for _ in range(self._max_iterations):


            response = context.llm_response


            if response is None:
                raise RuntimeError(
                    "LLM response missing before agent loop."
                )

            logger.info(
                "Agent loop response",
                extra={
                    "tool_calls": response.tool_calls,
                    "content": response.content,
                },
            )



            #
            # No tool call:
            # Agent finished
            #
            if not response.tool_calls:


                context.response = (
                    response.content or ""
                )


                return context.response



            #
            # Add assistant tool request
            #
            messages.append(
                Message(
                    role="assistant",
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )



            #
            # Execute tools
            #
            for tool_call in response.tool_calls:


                with self._tracer.span(
                    trace,
                    "tool_call",
                    {
                        "tool": tool_call.name,
                    },
                ):


                    tool_result = (
                        await self._tool_step.execute_tool(
                            tool_name=tool_call.name,
                            arguments=tool_call.arguments,
                        )
                    )



                if tool_result.success:

                    tool_content = (
                        tool_result.content or ""
                    )


                else:

                    tool_content = (
                        "Tool execution failed: "
                        f"{tool_result.error}"
                    )



                #
                # Add tool result back to conversation
                #
                messages.append(
                    Message(
                        role="tool",
                        content=tool_content,
                        tool_call_id=tool_call.id,
                    )
                )



            #
            # Ask LLM again after tool result
            #
            with self._tracer.span(
                trace,
                "llm_call",
            ):

                await self._llm_step.execute(
                    context
                )



        raise RuntimeError(
            "Agent loop exceeded maximum iterations."
        )