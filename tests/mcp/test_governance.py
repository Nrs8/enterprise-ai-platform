"""
Tests for MCP governance.

Covers:
- allowed execution
- denied tools
- tenant isolation
- missing policy
"""

from __future__ import annotations


import pytest


from app.mcp.policy import (
    MCPPolicy,
)

from app.mcp.governance import (
    MCPPermissionChecker,
    MCPPermissionError,
)



def create_checker() -> MCPPermissionChecker:
    """
    Create permission checker fixture.
    """

    policy = MCPPolicy(
        server_name="calculator",
        allowed_tools=[
            "calculator",
        ],
        tenant_scope=[
            "tenant-a",
        ],
    )

    return MCPPermissionChecker(
        policies={
            "calculator": policy,
        }
    )



def test_permission_allows_valid_request():
    """
    Valid tenant and tool should pass.
    """

    checker = create_checker()


    result = checker.check(
        tenant_id="tenant-a",
        server_name="calculator",
        tool_name="calculator",
    )


    assert result is True



def test_permission_denies_unknown_tool():
    """
    Unknown tool should fail.
    """

    checker = create_checker()


    with pytest.raises(
        MCPPermissionError
    ):
        checker.check(
            tenant_id="tenant-a",
            server_name="calculator",
            tool_name="search",
        )



def test_permission_denies_unknown_tenant():
    """
    Unknown tenant should fail.
    """

    checker = create_checker()


    with pytest.raises(
        MCPPermissionError
    ):
        checker.check(
            tenant_id="tenant-b",
            server_name="calculator",
            tool_name="calculator",
        )



def test_permission_denies_missing_policy():
    """
    Missing server policy should fail.
    """

    checker = MCPPermissionChecker(
        policies={}
    )


    with pytest.raises(
        MCPPermissionError
    ):
        checker.check(
            tenant_id="tenant-a",
            server_name="unknown",
            tool_name="calculator",
        )