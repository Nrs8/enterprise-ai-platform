from dataclasses import dataclass


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
    """

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a query.
        """

        raise NotImplementedError