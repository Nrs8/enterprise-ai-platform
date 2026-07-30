from knowledge.models import Chunk, Document


class TextChunker:
    """
    Splits documents into fixed-size text chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        self._chunk_size = chunk_size
        self._overlap = overlap

    def split(
        self,
        document: Document,
    ) -> list[Chunk]:
        """
        Split a document into overlapping chunks.
        """

        content = document.content

        chunks: list[Chunk] = []

        start = 0
        chunk_index = 0

        while start < len(content):
            end = start + self._chunk_size

            chunk_content = content[start:end]

            chunks.append(
                Chunk(
                    chunk_id=f"{document.document_id}-{chunk_index}",
                    document_id=document.document_id,
                    content=chunk_content,
                    metadata=document.metadata,
                )
            )

            chunk_index += 1

            start = end - self._overlap

        return chunks