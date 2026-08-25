"""
Example MCP calculator server.

Simulates an external MCP server
providing calculator capability.
"""

from __future__ import annotations


from typing import Any, Dict, List


from app.mcp.models import (
    MCPTool,
    MCPToolCall,
    MCPToolResult,
)




class CalculatorMCPServer:
    """
    MCP calculator server.

    This is an isolated MCP service.
    """


    def list_tools(
        self,
    ) -> List[MCPTool]:
        """
        Return available tools.
        """

        return [
            MCPTool(
                name="mcp_calculator",
                description=(
                    "Calculate arithmetic expression"
                ),
                parameters={
                    "expression": "string"
                },
            )
        ]



    async   def call_tool(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:
        """
        Execute calculator tool.
        """

        if request.tool_name != (
            "mcp_calculator"
        ):

            return MCPToolResult(
                success=False,
                error="Unknown tool",
            )


        expression = (
            request.arguments.get(
                "expression"
            )
        )


        try:

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
            )


            return MCPToolResult(
                success=True,
                output=result,
            )


        except Exception as exc:

            return MCPToolResult(
                success=False,
                error=str(exc),
            )