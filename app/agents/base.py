from abc import ABC, abstractmethod

from app.runtime.context import AgentContext


class BaseAgent(ABC):
    """
    Base interface for all agents.
    """

    name: str = ""

    description: str = ""


    @abstractmethod
    async def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute agent responsibility.
        """
        pass