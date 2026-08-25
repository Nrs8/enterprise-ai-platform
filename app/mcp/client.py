"""
MCP client abstraction.

Provides client-side access to MCP servers.

The client communicates through
MCPTransport abstraction.

Supports:

- Local transport
- Future HTTP transport
- Future stdio transport
"""

from __future__ import annotations


from typing import List


from app.mcp.models import (
    MCPTool,
    MCPToolCall,
    MCPToolResult,
)


from app.mcp.transport import (
    MCPTransport,
)


from app.mcp.exceptions import (
    MCPConnectionError,
    MCPToolExecutionError,
)



class MCPClient:
    """
    Client for interacting with MCP servers.

    Responsibilities:

    - discover tools
    - execute tool calls
    - hide transport details

    Does not know:

    - local server
    - HTTP
    - websocket
    """



    def __init__(
        self,
    ) -> None:

        self._transport: MCPTransport | None = None



    def connect(
        self,
        transport: MCPTransport,
    ) -> None:
        """
        Connect MCP transport.

        Example:

            client.connect(
                LocalMCPTransport(server)
            )
        """

        try:

            self._transport = transport


        except Exception as exc:

            raise MCPConnectionError(
                "Failed to connect MCP transport"
            ) from exc



    def list_tools(
        self,
    ) -> List[MCPTool]:
        """
        Discover available MCP tools.
        """

        self._ensure_connected()


        try:

            return (
                self._transport.list_tools()
            )


        except Exception as exc:

            raise MCPConnectionError(
                "Failed to discover MCP tools"
            ) from exc



    async def call_tool(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:
        """
        Execute MCP tool call.
        """

        self._ensure_connected()


        try:

            return await (
                self._transport.call_tool(
                    request
                )
            )


        except MCPToolExecutionError:

            raise


        except Exception as exc:

            raise MCPToolExecutionError(
                "MCP tool execution failed"
            ) from exc



    async def close(
        self,
    ) -> None:
        """
        Close MCP transport.
        """

        if self._transport is None:

            return


        await (
            self._transport.close()
        )


        self._transport = None



    def _ensure_connected(
        self,
    ) -> None:
        """
        Validate transport connection.
        """

        if self._transport is None:

            raise MCPConnectionError(
                "MCP client is not connected"
            )