"""
MCP factory.

Creates MCP components
for application container.
"""

from __future__ import annotations


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

from app.mcp.server import (
    MCPServer,
)

from app.mcp.policy import (
    MCPPolicy,
)

from app.mcp.governance import (
    MCPPermissionChecker,
)

from app.tools.registry import (
    ToolRegistry,
)



def create_mcp_client(
    server: MCPServer,
) -> MCPClient:
    """
    Create MCP client.

    Client communicates with MCP server
    through transport.
    """

    transport = LocalMCPTransport(
        server
    )

    client = MCPClient()

    client.connect(
        transport
    )

    return client





def create_mcp_registry(
    server_name: str,
    client: MCPClient,
) -> MCPRegistry:
    """
    Create MCP registry.

    Registry manages MCP clients.
    """

    registry = MCPRegistry()


    registry.register(
        server_name,
        client,
    )


    return registry





def create_mcp_permission_checker(
    server_name: str,
) -> MCPPermissionChecker:
    """
    Create MCP permission checker.

    Creates default MCP policy.

    Production version can load
    policies from database.
    """

    policy = MCPPolicy(
        server_name=server_name,
        allowed_tools=[],
        tenant_scope=[],
        enabled=True,
    )


    return MCPPermissionChecker(
        policies={
            server_name: policy,
        }
    )





def create_mcp_bridge(
    tool_registry: ToolRegistry,
    server_name: str,
    server: MCPServer,
) -> MCPToolBridge:
    """
    Create MCP tool bridge.
    """


    client = create_mcp_client(
        server
    )


    registry = create_mcp_registry(
        server_name,
        client,
    )


    discovery = MCPDiscovery(
        registry
    )


    permission_checker = (
        create_mcp_permission_checker(
            server_name
        )
    )


    return MCPToolBridge(

        discovery=discovery,

        client=client,

        tool_registry=tool_registry,

        permission_checker=permission_checker,

        tenant_id="default",

        server_name=server_name,
    )