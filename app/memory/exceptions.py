"""
Custom exceptions for the memory module.
"""


class MemoryError(Exception):
    """
    Base exception for the memory module.
    """


class SessionNotFoundError(MemoryError):
    """
    Raised when a session cannot be found.
    """