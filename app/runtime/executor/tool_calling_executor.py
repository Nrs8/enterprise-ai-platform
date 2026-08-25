"""
Agent execution executor.

Responsible for:

    LLM
      |
      v
 Tool Calling
      |
      v
 Tool Execution
      |
      v
 LLM Again


Executes agent reasoning workflow.

The executor does NOT:

- manage memory persistence
- route agents
- store conversations

It only executes the reasoning workflow.
"""


from __future__ import annotations


import logging



logger = logging.getLogger(
    "app.runtime.executor"
)





class ToolCallingExecutor:
    """
    Executes iterative agent workflows.

    Execution flow:


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

    ) -> None:


        self._llm_step = llm_step

        self._tool_step = tool_step

        self._tracer = tracer

        self._max_iterations = (
            max_iterations
        )





    async def execute(

        self,

        context,

    ) -> str:
        """
        Execute agent workflow.
        """



        trace = context.trace




        for iteration in range(

            self._max_iterations

        ):



            logger.info(

                "Agent execution iteration %s",

                iteration + 1,

            )



            #
            # LLM reasoning
            #

            with self._tracer.span(

                trace,

                "llm_call",

            ):


                response = await (

                    self._llm_step.execute(

                        context

                    )

                )




            context.llm_response = response




            logger.info(

                "LLM response received",

                extra={

                    "tool_calls":

                        response.tool_calls,

                },

            )





            #
            # Final answer
            #

            if not response.tool_calls:


                context.set_response(

                    response.content or ""

                )


                return context.response





            #
            # Store assistant tool request
            #

            context.add_assistant_message(

                content=(

                    response.content or ""

                ),

                tool_calls=(

                    response.tool_calls

                ),

            )





            #
            # Execute tools
            #

            for tool_call in response.tool_calls:



                logger.info(

                    "Executing tool %s",

                    tool_call.name,

                )




                with self._tracer.span(

                    trace,

                    "tool_call",

                    {

                        "tool":

                            tool_call.name

                    },

                ):


                    result = await (

                        self._tool_step

                        .execute_tool(

                            tool_name=(

                                tool_call.name

                            ),

                            arguments=(

                                tool_call.arguments

                            ),

                        )

                    )





                if result.success:


                    content = (

                        result.content

                        or ""

                    )


                else:


                    content = (

                        "Tool execution failed: "

                        +

                        str(

                            result.error

                        )

                    )





                #
                # Feed tool result
                #

                context.add_tool_message(

                    content=content,

                    tool_call_id=(

                        tool_call.id

                    ),

                )





        raise RuntimeError(

            "Agent execution exceeded maximum iterations."

        )