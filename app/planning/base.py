"""
Planning interfaces.

Defines planner abstraction.
"""


from abc import ABC, abstractmethod


from app.runtime.context import AgentContext

from app.planning.models import (
    ExecutionPlan,
)



class Planner(ABC):
    """
    Abstract planner interface.
    """



    @abstractmethod
    async def create_plan(
        self,
        context: AgentContext,
    ) -> ExecutionPlan:
        """
        Create execution plan.
        """

        pass