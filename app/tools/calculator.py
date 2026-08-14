"""
Calculator tool implementation.
"""

from typing import Any

from app.tools.base import BaseTool


class CalculatorTool(BaseTool):

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Calculate a mathematical expression."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to calculate.",
                },
            },
            "required": ["expression"],
        }

    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> str:

        expression = arguments["expression"]

        result = eval(expression)

        return str(result)