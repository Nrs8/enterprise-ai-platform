"""
MCP transport abstraction.

Defines communication boundary
between MCP client and MCP server.

Future implementations:

- HTTP transport
- WebSocket transport
- stdio transport
"""

from __future__ import annotations


from abc import ABC, abstractmethod

from typing import List


from app.mcp.models import (
    MCPTool,
    MCPToolCall,
    MCPToolResult,
)



class MCPTransport(ABC):
    """
    Abstract MCP transport.

    MCPClient depends on this interface,
    not concrete server implementation.
    """



    @abstractmethod
    def list_tools(
        self,
    ) -> List[MCPTool]:
        """
        Discover MCP tools.
        """

        raise NotImplementedError



    @abstractmethod
    async def call_tool(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:
        """
        Execute MCP tool.
        """

        raise NotImplementedError



    @abstractmethod
    async def close(
        self,
    ) -> None:
        """
        Close transport resources.

        Implementations may release:

        - HTTP sessions
        - websocket connections
        - stdio processes
        - local resources
        """

        raise NotImplementedError