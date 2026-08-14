"""
LLM cost calculation.
"""

from dataclasses import dataclass


@dataclass
class ModelPricing:
    """
    Pricing information for one model.

    Cost unit:
    USD per 1K tokens.
    """

    input_price: float

    output_price: float


class CostCalculator:
    """
    Calculate LLM request cost.
    """


    PRICING = {

        "qwen3.7-plus": {

            "input": 0.00001,

            "output": 0.00002,

        },

        "fake-model": {

            "input": 0,

            "output": 0,

        }

    }


    def calculate(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:


        price = self.PRICING.get(
            model
        )


        if not price:
            return 0.0


        return (
            input_tokens * price["input"]
            +
            output_tokens * price["output"]
        )