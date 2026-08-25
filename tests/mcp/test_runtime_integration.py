"""
MCP runtime integration tests.

Validates end-to-end MCP execution flow.
"""


import pytest


from app.container import Container



@pytest.mark.asyncio
async def test_mcp_runtime_tool_execution():

    container = Container()


    runtime = container.runtime


    result = await runtime.chat(
        session_id="mcp-test-session",
        message="calculate 8 * 6",
        user_id="enterprise_user",
    )


    assert result is not None


    assert (
        "48" in str(result)
        or
        "48" in str(result.response)
    )