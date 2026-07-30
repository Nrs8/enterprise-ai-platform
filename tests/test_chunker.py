from knowledge.chunker import TextChunker
from knowledge.models import Document  

def test_chunker_splits_document_into_chunks():
    document = Document(
        document_id="doc-1",
        content="a" * 1000,
        metadata={},
    )

    chunker = TextChunker(
        chunk_size=500,
        overlap=50,
    )

    chunks = chunker.split(document)

    assert len(chunks) == 3
    assert chunks[0].content == "a" * 500
    assert chunks[1].content == "a" * 500


def test_chunker_splits_document_into_chunks():
    document = Document(
        document_id="doc-1",
        content="a" * 1000,
        metadata={},
    )

    chunker = TextChunker(
        chunk_size=500,
        overlap=50,
    )

    chunks = chunker.split(document)

    assert len(chunks) == 3
    assert chunks[0].content == "a" * 500
    assert chunks[1].content == "a" * 500