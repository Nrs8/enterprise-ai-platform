"""
Tool registry implementation.
"""
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# 获取logger实例
logger = logging.getLogger(__name__)
from app.observability.metrics import metrics
from typing import Any

from app.tools.base import BaseTool
from app.tools.exceptions import ToolNotFoundError
from app.resilience.retry import retry
from app.resilience.timeout import timeout

class ToolRegistry:
    """
    Stores and resolves available tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        self._tools[tool.name] = tool

    def get(
        self,
        name: str,
    ) -> BaseTool:
        try:
            return self._tools[name]

        except KeyError as exc:
            raise ToolNotFoundError(
                f"Tool '{name}' is not registered."
            ) from exc

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str:
        metrics.increment(
            "tool_calls"
        )
        tool = self.get(tool_name)

        return await retry(
            timeout,
            tool.execute,
            arguments,
        )

    def get_schemas(self) -> list[dict[str, Any]]:
        return [
            tool.schema()
            for tool in self._tools.values()
        ]