"""
Tests for AgentRuntime.

Covers:

- successful execution
- agent not found
- agent failure
- assistant message persistence
"""


from __future__ import annotations


import pytest


from app.agents.models import (
    AgentResult,
)


from app.runtime.errors import (
    RuntimeErrorInfo,
    ErrorCategory,
)



# ============================================================
# Runtime Success
# ============================================================


@pytest.mark.asyncio
async def test_runtime_chat_success(
    runtime,
    runtime_dependencies,
):
    """
    Runtime executes full agent lifecycle.
    """


    result = await runtime.chat(

        session_id="session-1",

        message="hello",

    )


    assert result.success is True

    assert result.response == "hello"





# ============================================================
# Agent Not Found
# ============================================================


@pytest.mark.asyncio
async def test_runtime_agent_not_found(
    runtime,
    runtime_dependencies,
):
    """
    Runtime returns structured error
    when supervisor selects unknown agent.
    """


    runtime_dependencies[
        "registry"
    ].get.return_value = None



    result = await runtime.chat(

        session_id="session-1",

        message="hello",

    )



    assert result.success is False


    assert result.error is not None


    assert result.error.code == (
        "internal_error"
    )





# ============================================================
# Agent Failure
# ============================================================


@pytest.mark.asyncio
async def test_runtime_agent_failure(
    runtime,
    runtime_dependencies,
):
    """
    Runtime returns agent execution failure.
    """


    runtime_dependencies[
        "executor"
    ].execute.return_value = AgentResult(

        success=False,

        error=RuntimeErrorInfo(

            code=(
                "tool_execution_failed"
            ),

            message="failed",

            category=(
                ErrorCategory.TOOL_FAILURE
            ),

            retryable=False,

        ),

    )



    result = await runtime.chat(

        session_id="session-1",

        message="hello",

    )



    assert result.success is False


    assert result.error is not None


    assert result.error.message == (
        "failed"
    )





# ============================================================
# Persistence
# ============================================================


@pytest.mark.asyncio
async def test_runtime_persist_assistant_message(
    runtime,
    runtime_dependencies,
):
    """
    Runtime persists assistant response.
    """


    await runtime.chat(

        session_id="session-1",

        message="hello",

    )


    memory = runtime_dependencies[
        "memory"
    ]


    memory.add_message.assert_called()