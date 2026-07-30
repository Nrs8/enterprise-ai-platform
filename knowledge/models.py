from dataclasses import dataclass


@dataclass
class Document:
    """
    A knowledge document.
    """

    document_id: str
    content: str
    metadata: dict


@dataclass
class Chunk:
    """
    A chunk extracted from a document.
    """

    chunk_id: str
    document_id: str
    content: str
    metadata: dict