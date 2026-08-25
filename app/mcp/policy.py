"""
MCP Permission Policy.

Defines MCP tool and tenant access rules.
"""

from __future__ import annotations


from typing import List, Optional



class MCPPolicy:
    """
    MCP access policy.

    Controls:

    - enabled state
    - allowed tools
    - denied tools
    - tenant scope
    """

    def __init__(
        self,
        server_name: str | None = None,
        allowed_tools: Optional[List[str]] = None,
        denied_tools: Optional[List[str]] = None,
        tenant_scope: Optional[List[str]] = None,
        enabled: bool = True,
    ) -> None:

        self.server_name = server_name

        self.allowed_tools = (
            allowed_tools
            or []
        )

        self.denied_tools = (
            denied_tools
            or []
        )

        self.tenant_scope = (
            tenant_scope
            or []
        )

        self.enabled = enabled



    def allow(
        self,
        tool_name: str,
    ) -> None:
        """
        Add tool to allow list.
        """

        if tool_name not in self.allowed_tools:
            self.allowed_tools.append(
                tool_name
            )



    def deny(
        self,
        tool_name: str,
    ) -> None:
        """
        Add tool to deny list.
        """

        if tool_name not in self.denied_tools:
            self.denied_tools.append(
                tool_name
            )



    def allows_tool(
        self,
        tool_name: str,
    ) -> bool:
        """
        Check tool permission.
        """


        if not self.enabled:
            return False


        #
        # deny rule has priority
        #

        if tool_name in self.denied_tools:
            return False


        #
        # empty allow list means
        # no restriction
        #

        if not self.allowed_tools:
            return True


        return (
            tool_name
            in self.allowed_tools
        )



    def allows_tenant(
        self,
        tenant_id: str,
    ) -> bool:
        """
        Check tenant permission.
        """

        if not self.enabled:
            return False


        #
        # empty scope means
        # all tenants allowed
        #

        if not self.tenant_scope:
            return True


        return (
            tenant_id
            in self.tenant_scope
        )



    def check_permission(
        self,
        user_id: str | None = None,
        tool_name: str | None = None,
        tenant_id: str | None = None,
        server_name: str | None = None,
    ) -> bool:
        """
        Evaluate complete permission.
        """

        if tool_name is None:
            return False


        if not self.allows_tool(
            tool_name
        ):
            return False


        if tenant_id is not None:

            if not self.allows_tenant(
                tenant_id
            ):
                return False


        return True