"""
Calculator tool implementation.

Provides safe mathematical expression
evaluation for Agent tool calling.
"""


from __future__ import annotations


import ast
import operator

from typing import Any


from app.tools.base import BaseTool





class CalculatorTool(BaseTool):
    """
    Mathematical calculator tool.

    Implements BaseTool contract.

    Responsibilities:

    - Expose tool metadata
    - Validate arguments
    - Execute calculation

    Does NOT:

    - Call LLM
    - Manage memory
    - Perform reasoning
    """



    _operators = {

        ast.Add:
            operator.add,

        ast.Sub:
            operator.sub,

        ast.Mult:
            operator.mul,

        ast.Div:
            operator.truediv,

        ast.Pow:
            operator.pow,

    }





    @property
    def name(
        self,
    ) -> str:
        """
        Tool name.
        """

        return "calculator"





    @property
    def description(
        self,
    ) -> str:
        """
        Tool description.
        """

        return (
            "Calculate a mathematical "
            "expression."
        )





    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        """
        OpenAI compatible tool schema.
        """

        return {

            "type": "object",

            "properties": {

                "expression": {

                    "type": "string",

                    "description":
                        "Mathematical expression.",

                }

            },

            "required": [

                "expression"

            ],

        }





    def _calculate(
        self,
        node: ast.AST,
    ) -> Any:
        """
        Recursively evaluate AST.

        Supports:

        - numbers
        - +
        - -
        - *
        - /
        - **

        """



        if isinstance(
            node,
            ast.Constant,
        ):

            return node.value





        if isinstance(
            node,
            ast.BinOp,
        ):


            left = self._calculate(
                node.left
            )


            right = self._calculate(
                node.right
            )


            operator_func = (
                self._operators.get(
                    type(node.op)
                )
            )


            if operator_func is None:

                raise ValueError(
                    "Unsupported operator"
                )


            return operator_func(
                left,
                right,
            )





        raise ValueError(
            "Unsupported expression"
        )






    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> str:
        """
        Execute calculation.
        """



        expression = arguments.get(
            "expression"
        )


        if not expression:

            raise ValueError(
                "Missing expression"
            )



        tree = ast.parse(
            expression,
            mode="eval",
        )



        result = self._calculate(
            tree.body
        )



        return str(result)