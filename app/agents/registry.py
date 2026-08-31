"""
Agent registry.

Responsible for managing available agents
inside the runtime.
"""

from __future__ import annotations

from app.agents.base import BaseAgent



class AgentRegistry:
    """
    Registry for managing agents.

    The registry provides agent discovery
    and lifecycle management for AgentRuntime.
    """


    def __init__(self) -> None:
        """
        Initialize registry.
        """

        self._agents: dict[str, BaseAgent] = {}



    def register(
        self,
        agent: BaseAgent,
    ) -> None:
        """
        Register an agent.

        Raises:
            ValueError:
                If agent name already exists.
        """

        if agent.name in self._agents:
            raise ValueError(
                f"Agent already registered: {agent.name}"
            )

        self._agents[agent.name] = agent



    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove an agent from registry.
        """

        if name not in self._agents:
            raise ValueError(
                f"Agent not found: {name}"
            )

        del self._agents[name]



    def get(
        self,
        name: str,
    ) -> BaseAgent:
        """
        Retrieve an agent.

        Raises:
            ValueError:
                If agent does not exist.
        """

        agent = self._agents.get(name)

        if agent is None:
            raise ValueError(
                f"Agent not found: {name}"
            )

        return agent



    def has(
        self,
        name: str,
    ) -> bool:
        """
        Check whether an agent exists.
        """

        return name in self._agents



    def list_agents(self) -> list[str]:
        """
        List registered agents.
        """

        return list(
            self._agents.keys()
        )