from app.runtime.steps.base import AgentStep


class RetrieveStep(AgentStep):
    """
    Retrieve relevant knowledge from knowledge base.
    """

    def __init__(
        self,
        knowledge_base,
    ):
        self._knowledge_base = knowledge_base


    async def execute(
        self,
        context,
    ) -> None:

        chunks = self._knowledge_base.search(
            query=context.input,
            top_k=3,
        )

        context.knowledge_context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )