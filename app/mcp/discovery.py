"""
MCP tool discovery.

Responsible for discovering tools
provided by MCP servers.
"""

from __future__ import annotations


from typing import List


from app.mcp.models import MCPTool
from app.mcp.registry import MCPRegistry




class MCPDiscovery:
    """
    Discovers tools from registered
    MCP servers.
    """


    def __init__(
        self,
        registry: MCPRegistry,
    ) -> None:

        self.registry = registry



    def discover_tools(
        self,
    ) -> List[MCPTool]:
        """
        Discover all tools from
        registered MCP servers.
        """

        tools: List[MCPTool] = []


        for server_name in (
            self.registry.list_servers()
        ):

            server = self.registry.get(
                server_name
            )

            tools.extend(
                server.list_tools()
            )


        return tools