"""
MCP exceptions.

Defines MCP specific errors.
"""


class MCPException(Exception):
    """
    Base MCP exception.
    """

    pass


class MCPConnectionError(
    MCPException
):
    """
    MCP connection failure.
    """

    pass


class MCPToolExecutionError(
    MCPException
):
    """
    MCP tool execution failure.
    """

    pass


class MCPPermissionDenied(
    MCPException
):
    """
    MCP permission denied.
    """

    pass