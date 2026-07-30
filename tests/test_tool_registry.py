from app.tools.calculator import CalculatorTool
from app.tools.registry import ToolRegistry


def test_registry_registers_and_resolves_tool():
    registry = ToolRegistry()
    calculator = CalculatorTool()

    registry.register(calculator)

    resolved_tool = registry.get("calculator")

    assert resolved_tool is calculator

def test_registry_returns_tool_schemas():
    registry = ToolRegistry()

    registry.register(CalculatorTool())

    schemas = registry.get_schemas()

    assert len(schemas) == 1
    assert schemas[0]["type"] == "function"
    assert schemas[0]["function"]["name"] == "calculator"