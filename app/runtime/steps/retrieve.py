from __future__ import annotations


from app.runtime.steps.base import AgentStep

from knowledge.retriever import Retriever





class RetrieveStep(AgentStep):
    """
    Retrieve relevant knowledge from knowledge base.

    Responsibilities:

    - Receive query from AgentContext
    - Call Retriever
    - Inject knowledge context

    Does NOT:

    - Manage embeddings
    - Manage vector store
    - Manage documents
    """



    def __init__(
        self,
        retriever: Retriever,
    ) -> None:

        self._retriever = retriever





    async def execute(
        self,
        context,
    ) -> None:
        """
        Retrieve knowledge and update context.
        """


        chunks = self._retriever.retrieve(
            query=context.input,
            top_k=3,
        )


        context.knowledge_context = (
            "\n\n".join(
                chunk.content
                for chunk in chunks
            )
        )