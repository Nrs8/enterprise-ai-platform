"""
Tool-related domain exceptions.
"""


class ToolError(Exception):
    """
    Base exception for tool-related errors.
    """


class ToolNotFoundError(ToolError):
    """
    Raised when a requested tool is not registered.
    """