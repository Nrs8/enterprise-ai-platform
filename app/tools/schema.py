"""
Tool schema converters.

Internal tool schema ->
OpenAI compatible function schema.
"""

from __future__ import annotations


from typing import Any





def convert_tool_schema(
    schema: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert internal schema.

    From:

    {
        name,
        description,
        parameters
    }


    To:

    {
        type:"function",
        function:{
            name,
            description,
            parameters
        }
    }
    """

    return {

        "type": "function",

        "function": {

            "name": schema.get(
                "name"
            ),

            "description": schema.get(
                "description",
                "",
            ),

            "parameters": schema.get(
                "parameters",
                {},
            ),
        },
    }





def convert_tools(
    tools: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Convert list of tools.
    """

    return [
        convert_tool_schema(
            tool
        )
        for tool in tools
    ]