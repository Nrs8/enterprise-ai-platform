from dataclasses import dataclass

from knowledge.models import Chunk


@dataclass
class VectorRecord:
    """
    Stores a chunk and its embedding vector.
    """

    chunk: Chunk
    embedding: list[float]


class InMemoryVectorStore:
    """
    Simple in-memory vector store for MVP.
    """

    def __init__(self) -> None:
        self._records: list[VectorRecord] = []

    def add(
        self,
        chunk: Chunk,
        embedding: list[float],
    ) -> None:
        """
        Store a chunk and its embedding.
        """

        self._records.append(
            VectorRecord(
                chunk=chunk,
                embedding=embedding,
            )
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorRecord]:
        """
        Return the most similar records.
        """

        # 暂时使用简单的点积相似度
        scored_records = []

        for record in self._records:
            score = sum(
                query_value * document_value
                for query_value, document_value in zip(
                    query_embedding,
                    record.embedding,
                )
            )

            scored_records.append(
                (score, record)
            )

        scored_records.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            record
            for _, record in scored_records[:top_k]
        ]