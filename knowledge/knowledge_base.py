from knowledge.embedder import SimpleEmbedder
from knowledge.models import Chunk, Document
from knowledge.vector_store import InMemoryVectorStore


class KnowledgeBase:
    """
    Coordinates document ingestion and retrieval.
    """

    def __init__(
        self,
        embedder: SimpleEmbedder,
        vector_store: InMemoryVectorStore,
    ) -> None:
        self._embedder = embedder
        self._vector_store = vector_store

    def add_document(
        self,
        document: Document,
        chunks: list[Chunk],
    ) -> None:
        """
        Add document chunks to the knowledge base.
        """

        for chunk in chunks:
            embedding = self._embedder.embed(
                chunk.content
            )

            self._vector_store.add(
                chunk=chunk,
                embedding=embedding,
            )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Chunk]:
        """
        Search the knowledge base.
        """

        query_embedding = self._embedder.embed(query)

        records = self._vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return [
            record.chunk
            for record in records
        ]