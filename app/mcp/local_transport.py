"""
Local MCP transport.

Provides in-memory communication
between MCP client and MCP server.
"""

from __future__ import annotations


from typing import List


from app.mcp.transport import (
    MCPTransport,
)


from app.mcp.models import (
    MCPTool,
    MCPToolCall,
    MCPToolResult,
)


from app.mcp.server import (
    MCPServer,
)



class LocalMCPTransport(
    MCPTransport
):
    """
    Local in-memory transport.

    Used for:

    - development
    - testing
    - embedded MCP server
    """



    def __init__(
        self,
        server: MCPServer,
    ) -> None:

        self.server: MCPServer | None = server



    def list_tools(
        self,
    ) -> List[MCPTool]:
        """
        Discover tools.
        """

        self._ensure_server()


        return (
            self.server.list_tools()
        )



    async def call_tool(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:
        """
        Execute tool.
        """

        self._ensure_server()


        return await (
            self.server.call_tool(
                request
            )
        )



    async def close(
        self,
    ) -> None:
        """
        Close local transport.

        Local transport does not own
        external resources.

        Clears server reference only.
        """

        self.server = None



    def _ensure_server(
        self,
    ) -> None:
        """
        Validate server availability.
        """

        if self.server is None:

            raise RuntimeError(
                "MCP server is closed"
            )