"""
Knowledge retrieval module.

Provides retrieval abstraction over KnowledgeBase.
"""


from __future__ import annotations


from dataclasses import dataclass


from knowledge.knowledge_base import KnowledgeBase





@dataclass
class RetrievedChunk:
    """
    A chunk retrieved from the knowledge base.
    """

    content: str

    source: str

    score: float





class Retriever:
    """
    Retrieve relevant knowledge chunks.

    Flow:

        Query
          |
          v
      Retriever
          |
          v
    KnowledgeBase
          |
          v
    RetrievedChunk[]
    """



    def __init__(
        self,
        knowledge_base: KnowledgeBase,
    ) -> None:
        """
        Initialize retriever.

        Args:
            knowledge_base:
                Knowledge base used for searching.
        """

        self._knowledge_base = (
            knowledge_base
        )





    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant knowledge chunks.

        Args:
            query:
                User query.

            top_k:
                Maximum number of chunks.

        Returns:
            Retrieved knowledge chunks.
        """

        chunks = (
            self._knowledge_base.search(
                query,
                top_k,
            )
        )


        return [
            RetrievedChunk(
                content=chunk.content,
                source=chunk.document_id,
                score=0.0,
            )
            for chunk in chunks
        ]