"""
Tool Registry.

Central registry for
internal and MCP tools.
"""


from __future__ import annotations


import inspect

from typing import Any


from app.tools.base import (
    BaseTool,
)


from app.tools.exceptions import (
    ToolNotFoundError,
)





class ToolRegistry:
    """
    Central tool registry.

    Responsibilities:

    - Register tools
    - Discover tools
    - Execute tools
    - Export schemas
    """



    def __init__(
        self,
    ) -> None:

        self._tools: dict[
            str,
            BaseTool,
        ] = {}





    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool.

        Args:

            tool:
                Tool implementing BaseTool.
        """

        self._tools[
            tool.name
        ] = tool





    def get(
        self,
        name: str,
    ) -> BaseTool:
        """
        Get tool by name.

        Raises:

            ToolNotFoundError
        """

        tool = self._tools.get(
            name
        )


        if tool is None:

            raise ToolNotFoundError(
                f"Tool not found: {name}"
            )


        return tool





    def list_tools(
        self,
    ) -> list[str]:
        """
        Return registered tool names.
        """

        return list(
            self._tools.keys()
        )





    def get_schemas(
        self,
    ) -> list[dict[str, Any]]:
        """
        Export OpenAI compatible
        function calling schemas.


        Output example:


        [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "...",
                    "parameters": {}
                }
            }
        ]

        """

        schemas: list[
            dict[str, Any]
        ] = []


        for tool in self._tools.values():


            parameters = getattr(
                tool,
                "parameters",
                None,
            )


            if parameters is None:

                parameters = {

                    "type": "object",

                    "properties": {},

                }



            schema = {

                "type": "function",

                "function": {

                    "name": tool.name,

                    "description": getattr(
                        tool,
                        "description",
                        "",
                    ),

                    "parameters": parameters,

                },

            }


            schemas.append(
                schema
            )


        return schemas





    async def execute(
        self,
        name: str | None = None,
        arguments: dict[str, Any] | None = None,
        tool_name: str | None = None,
    ) -> Any:
        """
        Execute tool.


        Supports:


        execute(
            name="calculator",
            arguments={}
        )


        execute(
            tool_name="calculator",
            arguments={}
        )


        Supports:

        - sync tools
        - async tools
        - MCP proxy tools

        """



        target = (

            tool_name

            or name

        )



        if target is None:

            raise ToolNotFoundError(
                "Tool name is required"
            )



        tool = self.get(
            target
        )



        payload = (

            arguments

            or {}

        )



        #
        # Execute
        #
        # Most tools:
        #
        # execute(**kwargs)
        #
        # MCP proxy:
        #
        # execute(arguments)
        #
        

        try:

            result = tool.execute(
                **payload
            )


        except TypeError:

            result = tool.execute(
                payload
            )



        #
        # Await async result
        #

        if inspect.isawaitable(
            result
        ):

            return await result



        return result