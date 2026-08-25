"""
MCP tool adapter.

Exposes internal tools
as MCP tools.
"""

from __future__ import annotations


from typing import List


from app.tools.registry import (
    ToolRegistry,
)


from app.mcp.models import (
    MCPTool,
    MCPToolCall,
    MCPToolResult,
)



class MCPToolAdapter:
    """
    Adapts internal ToolRegistry
    into MCP tool interface.
    """



    def __init__(
        self,
        tool_registry: ToolRegistry,
    ) -> None:

        self.tool_registry = tool_registry



    def list_tools(
        self,
    ) -> List[MCPTool]:
        """
        Convert internal tools
        into MCP definitions.
        """

        tools = []


        for schema in (
            self.tool_registry.get_schemas()
        ):

            #
            # Support both:
            #
            # {
            #   name,
            #   description,
            #   parameters
            # }
            #
            # and:
            #
            # {
            #   type:function,
            #   function:{
            #       name,
            #       description,
            #       parameters
            #   }
            # }
            #

            function = schema.get(
                "function",
                schema,
            )


            tools.append(
                MCPTool(
                    name=function["name"],

                    description=function.get(
                        "description",
                        "",
                    ),

                    parameters=function.get(
                        "parameters",
                        {},
                    ),
                )
            )


        return tools



    async def call_tool(
        self,
        request: MCPToolCall,
    ) -> MCPToolResult:
        """
        Execute internal tool.
        """

        try:

            result = await (
                self.tool_registry.execute(
                    tool_name=request.tool_name,
                    arguments=request.arguments,
                )
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