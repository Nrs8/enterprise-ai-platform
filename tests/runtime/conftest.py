"""
Runtime test fixtures.

Provides:

- AgentRuntime dependencies
- Mock agents
- Mock executor
- Runtime instance

Shared by runtime tests.
"""


from __future__ import annotations


import pytest


from unittest.mock import (
    Mock,
    AsyncMock,
)


from app.agents.models import (
    AgentResult,
)


from app.runtime.runtime import (
    AgentRuntime,
)





# ============================================================
# Runtime Dependencies
# ============================================================


@pytest.fixture
def runtime_dependencies():
    """
    Create mocked runtime dependencies.
    """


    memory = Mock()


    context_builder = Mock()


    supervisor = AsyncMock()


    registry = Mock()


    executor = AsyncMock()


    executor.execute.return_value = AgentResult(

        success=True,

        response="hello",

        agent="fake_agent",

    )



    governance = AsyncMock()



    return {

        "memory": memory,

        "context_builder": context_builder,

        "supervisor": supervisor,

        "registry": registry,

        "executor": executor,

        "governance": governance,

    }





# ============================================================
# Agent Runtime
# ============================================================


@pytest.fixture
def runtime(
    runtime_dependencies,
):
    """
    Create AgentRuntime instance.
    """


    return AgentRuntime(

        memory_manager=(

            runtime_dependencies[
                "memory"
            ]

        ),


        context_builder=(

            runtime_dependencies[
                "context_builder"
            ]

        ),


        supervisor_agent=(

            runtime_dependencies[
                "supervisor"
            ]

        ),


        agent_registry=(

            runtime_dependencies[
                "registry"
            ]

        ),


        agent_executor=(

            runtime_dependencies[
                "executor"
            ]

        ),


        governance_step=(

            runtime_dependencies[
                "governance"
            ]

        ),

    )