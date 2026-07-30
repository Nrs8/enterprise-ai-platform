from knowledge.chunker import TextChunker
from knowledge.document_loader import DocumentLoader
from knowledge.models import Chunk


class KnowledgeIngestion:
    """
    Load documents and convert them into chunks.
    """

    def __init__(
        self,
        document_loader: DocumentLoader,
        chunker: TextChunker,
    ) -> None:
        self._document_loader = document_loader
        self._chunker = chunker

    def ingest(
        self,
        directory: str,
    ) -> list[Chunk]:
        """
        Load documents and split them into chunks.
        """

        documents = self._document_loader.load_directory(
            directory
        )

        chunks: list[Chunk] = []

        for document in documents:
            document_chunks = self._chunker.split(
                document
            )

            chunks.extend(document_chunks)

        return chunks