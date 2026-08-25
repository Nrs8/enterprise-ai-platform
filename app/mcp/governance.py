"""
MCP Governance.

Responsible for MCP authorization.
"""

from __future__ import annotations


from typing import Dict


from app.mcp.exceptions import (
    MCPPermissionDenied,
)


from app.mcp.policy import (
    MCPPolicy,
)



#
# compatibility alias
#

MCPPermissionError = MCPPermissionDenied



class MCPPermissionChecker:
    """
    MCP permission checker.

    Supports:

    - single policy
    - multi server policies
    """

    def __init__(
        self,
        policy: MCPPolicy | None = None,
        policies: Dict[str, MCPPolicy] | None = None,
    ) -> None:

        self.policy = policy

        self.policies = (
            policies
            or {}
        )



    def check(
        self,
        tenant_id: str,
        server_name: str,
        tool_name: str,
    ) -> bool:
        """
        Check MCP permission.
        """


        policy = self.policy


        if policy is None:

            policy = self.policies.get(
                server_name
            )


        if policy is None:

            raise MCPPermissionDenied(
                "Missing MCP policy"
            )


        if not policy.allows_tool(
            tool_name
        ):

            raise MCPPermissionDenied(
                f"Tool denied: {tool_name}"
            )


        if not policy.allows_tenant(
            tenant_id
        ):

            raise MCPPermissionDenied(
                f"Tenant denied: {tenant_id}"
            )


        return True



    def check_permission(
        self,
        user_id: str,
        tool_name: str,
        tenant_id: str | None = None,
        server_name: str | None = None,
    ) -> bool:
        """
        Compatibility API.
        """

        return self.check(
            tenant_id=tenant_id or "",
            server_name=(
                server_name
                or (
                    self.policy.server_name
                    if self.policy
                    else ""
                )
            ),
            tool_name=tool_name,
        )



class MCPGovernance:
    """
    Governance facade.
    """

    def __init__(
        self,
        checker: MCPPermissionChecker | None = None,
    ) -> None:

        self.checker = (
            checker
            or MCPPermissionChecker()
        )



    def authorize(
        self,
        tenant_id: str,
        server_name: str,
        tool_name: str,
    ) -> bool:
        """
        Authorize MCP request.
        """

        return self.checker.check(
            tenant_id=tenant_id,
            server_name=server_name,
            tool_name=tool_name,
        )