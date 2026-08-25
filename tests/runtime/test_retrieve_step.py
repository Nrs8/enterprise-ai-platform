"""
Tests for RetrieveStep.

Validates:

    AgentContext
          |
          v
    RetrieveStep
          |
          v
    Retriever
          |
          v
    knowledge_context
"""


from __future__ import annotations


import pytest


from app.runtime.context import AgentContext

from app.runtime.steps.retrieve import (
    RetrieveStep,
)

from knowledge.retriever import (
    RetrievedChunk,
)





class FakeRetriever:
    """
    Fake retriever for RetrieveStep testing.
    """

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Return fake retrieved chunks.
        """

        return [
            RetrievedChunk(
                content=(
                    "Python is a programming language."
                ),
                source="doc-1",
                score=0.9,
            )
        ]





@pytest.mark.asyncio
async def test_retrieve_step_injects_knowledge_context():
    """
    RetrieveStep should inject retrieved
    knowledge into AgentContext.
    """


    retriever = FakeRetriever()


    step = RetrieveStep(
        retriever
    )


    context = AgentContext(
        session_id="test-session",
        input="What is Python?",
    )


    await step.execute(
        context
    )


    assert (
        context.knowledge_context
        ==
        "Python is a programming language."
    )