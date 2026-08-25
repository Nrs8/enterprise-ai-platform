"""
Workflow node execution abstractions.

Defines the execution contract
between WorkflowEngine and actual node implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from app.workflow.state import WorkflowState


class WorkflowNodeExecutor(ABC):
    """
    Base interface for workflow node execution.

    Every workflow node executor must implement:

        execute()

    Examples:

        KnowledgeNodeExecutor

        ToolNodeExecutor

        LLMNodeExecutor
    """


    @abstractmethod
    async def execute(
        self,
        state: WorkflowState,
    ) -> Dict[str, Any]:
        """
        Execute node logic.

        Args:

            state:
                Current workflow runtime state.


        Returns:

            Node execution result.
        """

        pass



class FunctionNodeExecutor(
    WorkflowNodeExecutor
):
    """
    Generic function based node executor.

    Useful for lightweight workflow nodes.

    Example:

        async def handler(state):
            return {
                "value": 10
            }
    """


    def __init__(
        self,
        handler,
    ) -> None:

        self.handler = handler



    async def execute(
        self,
        state: WorkflowState,
    ) -> Dict[str, Any]:
        """
        Execute wrapped function.
        """

        result = await self.handler(
            state
        )

        return result