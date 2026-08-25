import pytest


from app.mcp.policy import (
    MCPPolicy,
)

from app.mcp.governance import (
    MCPPermissionChecker,
)

from app.mcp.exceptions import (
    MCPPermissionDenied,
)



def test_mcp_permission_allow():

    policy = MCPPolicy()

    policy.allow(
        "calculator"
    )


    checker = MCPPermissionChecker(
        policy
    )


    checker.check(
        tenant_id="tenant1",
        server_name="local",
        tool_name="calculator",
    )



def test_mcp_permission_deny():

    policy = MCPPolicy()


    policy.deny(
        "calculator"
    )


    checker = MCPPermissionChecker(
        policy
    )


    with pytest.raises(
        MCPPermissionDenied
    ):

        checker.check(
            tenant_id="tenant1",
            server_name="local",
            tool_name="calculator",
        )