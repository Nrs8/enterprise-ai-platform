"""
MCP Registry.

Stores MCP servers and clients.
"""

from __future__ import annotations


from typing import Any


from app.mcp.exceptions import (
    MCPException,
)





class MCPRegistry:
    """
    MCP server registry.

    Responsible for:

    - register MCP servers
    - lookup servers
    - lifecycle management
    """



    def __init__(
        self,
    ) -> None:

        self._servers: dict[
            str,
            Any,
        ] = {}





    def register(
        self,
        name: str,
        server: Any,
    ) -> None:
        """
        Register MCP server.
        """

        self._servers[
            name
        ] = server





    def get(
        self,
        name: str,
    ) -> Any:
        """
        Get MCP server.

        Raises when missing.
        """

        server = self._servers.get(
            name
        )


        if server is None:

            raise MCPException(
                f"MCP server not found: {name}"
            )


        return server





    def list_servers(
        self,
    ) -> list[str]:
        """
        List registered servers.
        """

        return list(
            self._servers.keys()
        )





    async def close(
        self,
    ) -> None:
        """
        Close all MCP servers/clients.
        """

        for server in self._servers.values():

            close = getattr(
                server,
                "close",
                None,
            )


            if close is not None:

                result = close()


                if hasattr(
                    result,
                    "__await__",
                ):
                    await result



        self._servers.clear()