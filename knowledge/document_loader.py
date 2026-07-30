from pathlib import Path
from uuid import uuid4

from knowledge.models import Document


class DocumentLoader:
    """
    Load Markdown knowledge documents from the filesystem.
    """

    def load_directory(
        self,
        directory: str,
    ) -> list[Document]:
        """
        Load all Markdown documents from a directory.
        """

        path = Path(directory)

        documents: list[Document] = []

        for file_path in path.rglob("*.md"):
            documents.append(
                Document(
                    document_id=str(uuid4()),
                    content=file_path.read_text(
                        encoding="utf-8",
                    ),
                    metadata={
                        "source": str(file_path),
                        "filename": file_path.name,
                        "domain": file_path.parent.name,
                    },
                )
            )

        return documents