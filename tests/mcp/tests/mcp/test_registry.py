"""
Tests for MCP registry.
"""

import pytest


from app.mcp.client import (
    MCPClient,
)


from app.mcp.registry import (
    MCPRegistry,
)



def test_register_and_get_client():
    """
    Test MCP client registration.
    """

    registry = MCPRegistry()

    client = MCPClient()


    registry.register(
        "calculator",
        client,
    )


    result = registry.get(
        "calculator"
    )


    assert result is client



def test_list_servers():
    """
    Test listing registered servers.
    """

    registry = MCPRegistry()


    registry.register(
        "calculator",
        MCPClient(),
    )


    registry.register(
        "knowledge",
        MCPClient(),
    )


    servers = registry.list_servers()


    assert "calculator" in servers
    assert "knowledge" in servers
    assert len(servers) == 2



def test_get_unknown_server():
    """
    Test unknown server handling.
    """

    registry = MCPRegistry()


    with pytest.raises(Exception):

        registry.get(
            "unknown"
        )



@pytest.mark.asyncio
async def test_close_registry():
    """
    Test closing all MCP clients.
    """

    registry = MCPRegistry()


    registry.register(
        "calculator",
        MCPClient(),
    )


    await registry.close()


    assert (
        registry.list_servers()
        == []
    )