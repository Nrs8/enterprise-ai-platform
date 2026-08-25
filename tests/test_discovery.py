"""
Tests MCP tool discovery.
"""

from app.mcp.registry import (
    MCPRegistry,
)

from app.mcp.discovery import (
    MCPDiscovery,
)

from app.mcp.servers.calculator_server import (
    CalculatorMCPServer,
)



def test_mcp_tool_discovery():

    registry = MCPRegistry()


    server = CalculatorMCPServer()


    registry.register(
        "calculator",
        server,
    )


    discovery = MCPDiscovery(
        registry
    )


    tools = (
        discovery.discover_tools()
    )


    names = [
        tool.name
        for tool in tools
    ]


    assert (
        "mcp_calculator"
        in names
    )