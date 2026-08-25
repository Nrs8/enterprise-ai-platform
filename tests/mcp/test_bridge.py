"""
Tests MCP tool bridge.

Verifies:

MCP Server
    |
    v
MCP Client
    |
    v
MCP Bridge
    |
    v
Tool Registry
"""

import pytest


from app.mcp.client import (
    MCPClient,
)


from app.mcp.local_transport import (
    LocalMCPTransport,
)


from app.mcp.registry import (
    MCPRegistry,
)


from app.mcp.discovery import (
    MCPDiscovery,
)


from app.mcp.bridge import (
    MCPToolBridge,
)


from app.tools.registry import (
    ToolRegistry,
)


from app.mcp.servers.calculator_server import (
    CalculatorMCPServer,
)



@pytest.mark.asyncio
async def test_mcp_tool_bridge():

    #
    # MCP Server
    #

    server = CalculatorMCPServer()



    #
    # MCP Registry
    #

    registry = MCPRegistry()


    registry.register(
        "calculator",
        server,
    )



    #
    # Discovery
    #

    discovery = MCPDiscovery(
        registry
    )



    #
    # MCP Client
    #

    client = MCPClient()


    client.connect(
        LocalMCPTransport(server)
    )



    #
    # Internal Tool Registry
    #

    tool_registry = ToolRegistry()



    #
    # Bridge
    #

    bridge = MCPToolBridge(

        discovery=discovery,

        client=client,

        tool_registry=tool_registry,

    )


    bridge.register_tools()



    #
    # Execute MCP Tool
    #

    result = await tool_registry.execute(

        tool_name="mcp_calculator",

        arguments={
            "expression": "8*6"
        },

    )



    #
    # Calculator MCP Server
    # returns integer result
    #

    assert result == 48