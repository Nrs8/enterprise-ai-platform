import pytest

from app.tools.calculator import CalculatorTool


@pytest.mark.asyncio
async def test_calculator_tool():
    tool = CalculatorTool()

    result = await tool.execute(
        {
            "expression": "2 + 2",
        }
    )

    assert result == "4"

