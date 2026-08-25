"""
Tests for AgentExecutor.
"""


import pytest


from app.agents.executor import AgentExecutor
from app.agents.models import AgentResult
from app.runtime.context import AgentContext





class SuccessAgent:
    """
    Agent returning successful result.
    """

    name = "success_agent"


    async def execute(
        self,
        context,
    ):

        return AgentResult(
            response="ok",
            success=True,
            agent=self.name,
        )





class FailureAgent:
    """
    Agent raising exception.
    """

    name = "failure_agent"


    async def execute(
        self,
        context,
    ):

        raise ValueError(
            "agent crashed"
        )





class ContextAgent:
    """
    Agent verifying context forwarding.
    """

    name = "context_agent"


    def __init__(self):

        self.received_context = None



    async def execute(
        self,
        context,
    ):

        self.received_context = context


        return AgentResult(
            response="ok",
            success=True,
            agent=self.name,
        )





@pytest.fixture
def context():

    return AgentContext(
        session_id="test-session",
        input="hello",
        model="fake",
        user_id="user",
        tenant_id="tenant",
    )





@pytest.mark.asyncio
async def test_agent_executor_success(
    context,
):

    executor = AgentExecutor()

    agent = SuccessAgent()


    result = await executor.execute(
        agent,
        context,
    )


    assert result.success is True
    assert result.response == "ok"
    assert result.agent == "success_agent"





@pytest.mark.asyncio
async def test_agent_executor_failure(
    context,
):

    executor = AgentExecutor()

    agent = FailureAgent()


    result = await executor.execute(
        agent,
        context,
    )


    assert result.success is False
    assert result.agent == "failure_agent"
    assert "agent crashed" in result.error





@pytest.mark.asyncio
async def test_agent_executor_forwards_context(
    context,
):

    executor = AgentExecutor()

    agent = ContextAgent()


    await executor.execute(
        agent,
        context,
    )


    assert agent.received_context is context





@pytest.mark.asyncio
async def test_agent_executor_returns_agent_result(
    context,
):

    executor = AgentExecutor()

    agent = SuccessAgent()


    result = await executor.execute(
        agent,
        context,
    )


    assert isinstance(
        result,
        AgentResult,
    )