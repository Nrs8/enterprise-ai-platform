"""
Tests MCP client communication.
"""

import pytest


from app.mcp.client import (
    MCPClient,
)


from app.mcp.models import (
    MCPToolCall,
)


from app.mcp.local_transport import (
    LocalMCPTransport,
)


from app.mcp.servers.calculator_server import (
    CalculatorMCPServer,
)



@pytest.mark.asyncio
async def test_mcp_client_call_tool():

    #
    # MCP Server
    #

    server = CalculatorMCPServer()



    #
    # Transport
    #

    transport = LocalMCPTransport(
        server
    )



    #
    # MCP Client
    #

    client = MCPClient()


    client.connect(
        transport
    )



    #
    # Discovery
    #

    tools = client.list_tools()


    assert len(tools) == 1


    assert (
        tools[0].name
        ==
        "mcp_calculator"
    )



    #
    # Execute MCP Tool
    #

    result = await client.call_tool(
        MCPToolCall(
            tool_name="mcp_calculator",
            arguments={
                "expression": "8*6"
            },
        )
    )



    assert result.success is True


    assert result.output == 48