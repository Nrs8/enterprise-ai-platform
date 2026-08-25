"""
Runtime memory flow tests.

Validates:

AgentRuntime
    |
    v
MemoryManager
    |
    v
Conversation persistence
    |
    v
ContextBuilder
    |
    v
Agent execution
"""


from __future__ import annotations


import pytest

from unittest.mock import (
    AsyncMock,
    Mock,
)


from app.runtime.runtime import AgentRuntime


from app.agents.models import (
    AgentResult,
)


from app.memory.models import (
    ConversationMemory,
    Message,
)


from app.memory.manager import (
    MemoryManager,
)


from app.runtime.context import (
    AgentContext,
)





# ============================================================
# Fake Memory Manager
# ============================================================


class FakeMemoryManager:
    """
    Lightweight memory manager for runtime tests.
    """


    def __init__(self):

        self.store: dict[
            str,
            ConversationMemory
        ] = {}



    def get_conversation(
        self,
        session_id: str,
    ):

        return self.store.get(
            session_id
        )



    def create_conversation(
        self,
        session_id: str,
        user_id: str,
    ):


        conversation = ConversationMemory(

            session_id=session_id,

            user_id=user_id,

            messages=[],

        )


        self.store[
            session_id
        ] = conversation


        return conversation



    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):


        conversation = self.store[
            session_id
        ]


        conversation.messages.append(

            Message(

                role=role,

                content=content,

            )

        )





# ============================================================
# Fake Components
# ============================================================


class FakeSupervisor:
    """
    Always selects fake_agent.
    """


    async def decide(
        self,
        context: AgentContext,
    ):


        return Mock(

            agent_name="fake_agent"

        )





class FakeRegistry:


    def get(
        self,
        name: str,
    ):

        return object()





class FakeExecutor:
    """
    Returns deterministic response.
    """


    async def execute(
        self,
        agent,
        context,
    ):


        return AgentResult.success_result(

            response=(

                "Hello, "

                + context.input

            ),

            agent="fake_agent",

        )





class FakeTracer:


    class Trace:


        trace_id = "test"

        spans = []



        def finish(self):

            pass



    class Span:


        def __enter__(
            self
        ):

            return self



        def __exit__(
            self,
            *args,
        ):

            pass



    def start_trace(
        self,
    ):

        return self.Trace()



    def span(
        self,
        trace,
        name,
    ):

        return self.Span()





# ============================================================
# Fixture
# ============================================================


@pytest.fixture
def runtime():


    memory_manager = FakeMemoryManager()


    context_builder = Mock()


    supervisor = FakeSupervisor()


    registry = FakeRegistry()


    executor = FakeExecutor()


    governance = Mock()


    governance.run = AsyncMock()



    return AgentRuntime(

        memory_manager=memory_manager,

        context_builder=context_builder,

        supervisor_agent=supervisor,

        agent_registry=registry,

        agent_executor=executor,

        governance_step=governance,

        tracer=FakeTracer(),

    )





# ============================================================
# Tests
# ============================================================


@pytest.mark.asyncio
async def test_runtime_persists_user_message(
    runtime,
):

    """
    User message should be persisted.
    """


    result = await runtime.chat(

        session_id="session-1",

        message="my name is Bob",

    )


    assert result.response == (

        "Hello, my name is Bob"

    )





    conversation = (

        runtime
        ._memory_manager
        .get_conversation(
            "session-1"
        )

    )


    assert conversation is not None


    assert len(
        conversation.messages
    ) == 2



    assert conversation.messages[0].role == "user"


    assert conversation.messages[0].content == (

        "my name is Bob"

    )



    assert conversation.messages[1].role == "assistant"





@pytest.mark.asyncio
async def test_runtime_loads_previous_history(
    runtime,
):

    """
    Runtime should reload previous
    conversation history.
    """


    session_id = "session-memory"



    first = await runtime.chat(

        session_id=session_id,

        message="my name is Bob",

    )


    assert first.response == (

        "Hello, my name is Bob"

    )



    second = await runtime.chat(

        session_id=session_id,

        message="what did I say?",

    )



    assert second.response == (

        "Hello, what did I say?"

    )



    conversation = (

        runtime
        ._memory_manager
        .get_conversation(
            session_id
        )

    )


    assert len(
        conversation.messages
    ) == 4



    assert conversation.messages[0].content == (

        "my name is Bob"

    )



    assert conversation.messages[2].content == (

        "what did I say?"

    )