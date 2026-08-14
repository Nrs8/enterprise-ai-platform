from app.agents.base import BaseAgent


class AgentRegistry:
    """
    Registry for managing agents.
    """


    def __init__(self) -> None:

        self._agents: dict[str, BaseAgent] = {}


    def register(
        self,
        agent: BaseAgent,
    ) -> None:
        """
        Register an agent.
        """

        self._agents[agent.name] = agent



    def get(
        self,
        name: str,
    ) -> BaseAgent:
        """
        Retrieve an agent.
        """

        if name not in self._agents:
            raise ValueError(
                f"Agent not found: {name}"
            )

        return self._agents[name]



    def list_agents(self) -> list[str]:
        """
        List registered agents.
        """

        return list(
            self._agents.keys()
        )