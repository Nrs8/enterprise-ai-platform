"""
MCP tool bridge.

Bridges MCP tools into
the internal tool execution system.
"""

from __future__ import annotations


import logging

from typing import Any, Optional


from app.mcp.audit import (
    MCPAuditEvent,
    MCPAuditLogger,
)


from app.mcp.client import (
    MCPClient,
)


from app.mcp.discovery import (
    MCPDiscovery,
)


from app.mcp.governance import (
    MCPPermissionChecker,
)


from app.mcp.exceptions import (
    MCPToolExecutionError,
)


from app.mcp.models import (
    MCPToolCall,
)


from app.tools.base import (
    BaseTool,
)



logger = logging.getLogger(
    "app.mcp.bridge"
)





class AllowAllPermissionChecker:
    """
    Default permission checker.

    Allows all MCP tool executions.
    """

    def check(
        self,
        tenant_id: str,
        server_name: str,
        tool_name: str,
    ) -> None:
        """
        Allow execution.
        """

        return





class MCPToolProxy(BaseTool):
    """
    Adapter between MCP tools and
    internal ToolRegistry.
    """



    def __init__(
        self,
        server_name: str,
        tool_name: str,
        description: str,
        parameters: dict[str, Any],
        client: MCPClient,
        permission_checker: Any,
        audit_logger: MCPAuditLogger,
        tenant_id: str,
    ) -> None:


        self._server_name = server_name

        self._name = tool_name

        self._description = description

        self._parameters = parameters

        self.client = client

        self.permission_checker = (
            permission_checker
        )

        self.audit_logger = (
            audit_logger
        )

        self.tenant_id = tenant_id



    @property
    def name(
        self,
    ) -> str:
        """
        Tool name.
        """

        return self._name



    @property
    def description(
        self,
    ) -> str:
        """
        Tool description.
        """

        return self._description



    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        """
        Tool parameters schema.
        """

        return self._parameters




    async def execute(
        self,
        arguments: Optional[
            dict[str, Any]
        ] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Execute MCP tool.

        Supports:

        execute(
            arguments={}
        )

        and:

        execute(
            key=value
        )
        """

        payload = (
            arguments
            if arguments is not None
            else kwargs
        )


        event = MCPAuditEvent(
            tenant_id=self.tenant_id,
            server_name=self._server_name,
            tool_name=self._name,
            success=False,
        )


        try:

            self.permission_checker.check(
                tenant_id=self.tenant_id,
                server_name=self._server_name,
                tool_name=self._name,
            )


            request = MCPToolCall(
                tool_name=self._name,
                arguments=payload,
            )


            result = await self.client.call_tool(
                request
            )


            if not result.success:

                raise MCPToolExecutionError(
                    result.error
                    or "MCP tool failed"
                )


            event.success = True


            return result.output



        except Exception as exc:

            event.error = str(
                exc
            )


            logger.exception(
                "MCP tool execution failed"
            )


            raise MCPToolExecutionError(
                str(exc)
            ) from exc



        finally:

            self.audit_logger.record(
                event
            )








class MCPToolBridge:
    """
    Converts MCP tools into
    internal executable tools.
    """



    def __init__(
        self,
        discovery: MCPDiscovery,
        client: MCPClient,
        tool_registry: Any,
        permission_checker: Optional[
            MCPPermissionChecker
        ] = None,
        tenant_id: str = "default",
        server_name: str = "local",
        audit_logger: Optional[
            MCPAuditLogger
        ] = None,
    ) -> None:


        self.discovery = discovery

        self.client = client

        self.tool_registry = tool_registry


        self.permission_checker = (
            permission_checker
            or AllowAllPermissionChecker()
        )


        self.tenant_id = tenant_id

        self.server_name = server_name


        self.audit_logger = (
            audit_logger
            or MCPAuditLogger()
        )





    def register_tools(
        self,
    ) -> None:
        """
        Discover MCP tools
        and register proxies.
        """


        tools = (
            self.discovery.discover_tools()
        )


        logger.info(
            "Discovered MCP tools=%s",
            tools,
        )



        for tool in tools:


            proxy = MCPToolProxy(

                server_name=self.server_name,

                tool_name=tool.name,

                description=tool.description,

                parameters=tool.parameters,

                client=self.client,

                permission_checker=(
                    self.permission_checker
                ),

                audit_logger=(
                    self.audit_logger
                ),

                tenant_id=(
                    self.tenant_id
                ),
            )



            self.tool_registry.register(
                proxy
            )


            logger.info(
                "Registered MCP tool=%s",
                proxy.name,
            )



        logger.info(
            "Tool registry=%s",
            self.tool_registry.list_tools(),
        )