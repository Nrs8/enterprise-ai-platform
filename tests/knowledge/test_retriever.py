from knowledge.models import (
    Chunk,
    Document,
)

from knowledge.knowledge_base import (
    KnowledgeBase,
)

from knowledge.embedder import (
    SimpleEmbedder,
)

from knowledge.vector_store import (
    InMemoryVectorStore,
)

from knowledge.retriever import (
    Retriever,
    RetrievedChunk,
)





def test_retriever_returns_chunks():

    embedder = SimpleEmbedder()

    vector_store = InMemoryVectorStore()

    knowledge_base = KnowledgeBase(
        embedder=embedder,
        vector_store=vector_store,
    )


    document = Document(
        document_id="doc-1",
        content="Python is a programming language",
        metadata={},
    )


    chunk = Chunk(
        chunk_id="chunk-1",
        document_id=document.document_id,
        content="Python is a programming language",
        metadata={},
    )


    knowledge_base.add_document(
        document=document,
        chunks=[chunk],
    )


    retriever = Retriever(
        knowledge_base
    )


    results = retriever.retrieve(
        "Python",
    )


    assert len(results) == 1

    assert isinstance(
        results[0],
        RetrievedChunk,
    )

    assert (
        results[0].content
        ==
        "Python is a programming language"
    )