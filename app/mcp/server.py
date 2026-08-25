"""
MCP server abstraction.

Provides MCP-compatible tool discovery
and execution interface.
"""

from __future__ import annotations


from typing import List


from app.mcp.models import (
    MCPTool,
    MCPToolCall,
    MCPToolResult,
)



class MCPServer:
    """
    MCP server wrapper.

    Delegates tool operations
    to adapter.
    """


    def __init__(
        self,
        tool_adapter,
    ) -> None:

        self.tool_adapter = tool_adapter



    def list_tools(
        self,
    ) -> List[MCPTool]:
        """
        Return available MCP tools.
        """

        return (
            self.tool_adapter.list_tools()
        )



    async def call_tool(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:
        """
        Execute MCP tool.
        """

        return await (
            self.tool_adapter.call_tool(
                request
            )
        )