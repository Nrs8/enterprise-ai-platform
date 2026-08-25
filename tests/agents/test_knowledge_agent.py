"""
Tests for KnowledgeAgent.
"""


from __future__ import annotations


import pytest


from app.agents.knowledge_agent import (
    KnowledgeAgent,
)

from app.llm.models import (
    LLMResponse,
)

from app.runtime.context import (
    AgentContext,
)





class FakeRetrieveStep:
    """
    Fake retrieve step.
    """


    async def execute(
        self,
        context,
    ) -> None:

        context.knowledge_context = (
            "Python is a programming language."
        )





class FakeLLMStep:
    """
    Fake LLM step.
    """


    async def execute(
        self,
        context,
    ) -> LLMResponse:

        return LLMResponse(
            content=(
                "Python is a popular "
                "programming language."
            ),
        )





@pytest.mark.asyncio
async def test_knowledge_agent_execute():

    agent = KnowledgeAgent(
        retrieve_step=FakeRetrieveStep(),
        llm_step=FakeLLMStep(),
    )


    context = AgentContext(
        session_id="test-session",
        input="What is Python?",
    )


    result = await agent.execute(
        context
    )


    assert result.success is True

    assert (
        result.agent
        ==
        "knowledge_agent"
    )

    assert (
        result.response
        ==
        "Python is a popular programming language."
    )

    assert (
        context.knowledge_context
        ==
        "Python is a programming language."
    )