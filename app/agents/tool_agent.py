from app.agents.base import BaseAgent

from app.runtime.context import AgentContext

from app.runtime.loop import AgentLoop

from app.runtime.steps.llm import LLMStep


class ToolAgent(BaseAgent):
    """
    Agent responsible for tool execution.

    Flow:

        LLMStep
          |
          v
        AgentLoop
          |
          +---- ToolStep
          |
          +---- LLMStep
    """

    name = "tool_agent"


    description = (
        "Handles tasks requiring tools."
    )


    def __init__(
        self,
        llm_step: LLMStep,
        agent_loop: AgentLoop,
    ) -> None:


        self.llm_step = llm_step

        self.agent_loop = agent_loop



    async def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute tool workflow.
        """


        #
        # First LLM reasoning
        #
        await self.llm_step.execute(
            context
        )


        #
        # Tool loop
        #
        response = await (
            self.agent_loop.run(
                context
            )
        )


        context.response = response


        return context