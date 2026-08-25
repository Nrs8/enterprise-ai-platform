"""
Tool agent workflow executor.

Adapts ToolAgent
to WorkflowEngine.
"""

from __future__ import annotations


from typing import Any, Dict


from app.workflow.node import (
    WorkflowNodeExecutor,
)

from app.workflow.state import (
    WorkflowState,
)



class ToolAgentExecutor(
    WorkflowNodeExecutor
):
    """
    Executes ToolAgent inside workflow.
    """


    def __init__(
        self,
        agent,
    ) -> None:

        self.agent = agent



    async def execute(
        self,
        state: WorkflowState,
    ) -> Dict[str, Any]:
        """
        Execute tool agent.
        """


        #
        # Recover AgentContext
        #
        # WorkflowState is workflow level state.
        # AgentContext is runtime level context.
        #

        context = (
            state.metadata.get(
                "context"
            )
        )


        if context is None:

            raise RuntimeError(
                "AgentContext missing "
                "from WorkflowState"
            )



        #
        # ToolAgent exposes execute()
        #

        result = await self.agent.execute(
            context
        )



        #
        # Save response
        #

        return {

            "response": (
                result.response
            ),


            "success": (
                result.success
            ),


            "agent": (
                result.agent
            ),


            "metadata": (
                result.metadata
            ),

        }