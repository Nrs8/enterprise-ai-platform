"""
Tests exporting internal tools
through MCP server.
"""

import pytest


from app.tools.registry import (
    ToolRegistry,
)


from app.tools.calculator import (
    CalculatorTool,
)


from app.mcp.adapter import (
    MCPToolAdapter,
)


from app.mcp.server import (
    MCPServer,
)


from app.mcp.client import (
    MCPClient,
)


from app.mcp.local_transport import (
    LocalMCPTransport,
)


from app.mcp.models import (
    MCPToolCall,
)



@pytest.mark.asyncio
async def test_mcp_server_export():

    #
    # Internal Tool System
    #

    tool_registry = ToolRegistry()


    tool_registry.register(
        CalculatorTool()
    )



    #
    # MCP Server
    #

    adapter = MCPToolAdapter(
        tool_registry
    )


    server = MCPServer(
        adapter
    )



    #
    # MCP Client
    #

    client = MCPClient()


    client.connect(
        LocalMCPTransport(server)
    )



    #
    # Discover
    #

    tools = client.list_tools()


    names = [
        tool.name
        for tool in tools
    ]


    assert (
        "calculator"
        in names
    )



    #
    # Execute
    #

    result = await client.call_tool(

        MCPToolCall(

            tool_name="calculator",

            arguments={
                "expression": "8*6"
            },

        )

    )


    assert result.success is True


    assert result.output == "48"