from app.runtime.context import AgentContext


class AgentStep:
    """
    Base class for agent execution steps.
    """

    async def execute(
        self,
        context: AgentContext,
    ) -> None:
        raise NotImplementedError