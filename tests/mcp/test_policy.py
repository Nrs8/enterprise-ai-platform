"""
Tests for MCP policy.

Covers:
- tool permission rules
- deny priority
- disabled policy
- tenant isolation
"""

from __future__ import annotations


from app.mcp.policy import (
    MCPPolicy,
)



def test_policy_allows_tool_when_allowed():
    """
    Allowed tool should pass.
    """

    policy = MCPPolicy(
        server_name="calculator",
        allowed_tools=[
            "calculator",
        ],
    )

    assert policy.allows_tool(
        "calculator"
    ) is True



def test_policy_denies_tool_when_not_allowed():
    """
    Tool outside allow list should fail.
    """

    policy = MCPPolicy(
        server_name="calculator",
        allowed_tools=[
            "calculator",
        ],
    )

    assert policy.allows_tool(
        "search"
    ) is False



def test_policy_deny_rule_has_priority():
    """
    Deny list overrides allow list.
    """

    policy = MCPPolicy(
        server_name="calculator",
        allowed_tools=[
            "calculator",
        ],
        denied_tools=[
            "calculator",
        ],
    )

    assert policy.allows_tool(
        "calculator"
    ) is False



def test_policy_disabled_denies_access():
    """
    Disabled policy rejects everything.
    """

    policy = MCPPolicy(
        server_name="calculator",
        enabled=False,
    )

    assert policy.allows_tool(
        "calculator"
    ) is False



def test_policy_allows_tenant_when_scope_empty():
    """
    Empty tenant scope means
    all tenants are allowed.
    """

    policy = MCPPolicy(
        server_name="calculator",
    )

    assert policy.allows_tenant(
        "tenant-a"
    ) is True



def test_policy_allows_configured_tenant():
    """
    Configured tenant should pass.
    """

    policy = MCPPolicy(
        server_name="calculator",
        tenant_scope=[
            "tenant-a",
        ],
    )

    assert policy.allows_tenant(
        "tenant-a"
    ) is True



def test_policy_denies_unknown_tenant():
    """
    Unknown tenant should fail.
    """

    policy = MCPPolicy(
        server_name="calculator",
        tenant_scope=[
            "tenant-a",
        ],
    )

    assert policy.allows_tenant(
        "tenant-b"
    ) is False