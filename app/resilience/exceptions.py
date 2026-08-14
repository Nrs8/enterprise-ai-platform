class AIPlatformError(Exception):
    """
    Base exception for AI platform.
    """
    pass


class LLMError(AIPlatformError):
    """
    LLM related failures.
    """
    pass


class ToolExecutionError(AIPlatformError):
    """
    Tool execution failures.
    """
    pass


class MemoryError(AIPlatformError):
    """
    Memory system failures.
    """
    pass