"""
Security and governance exceptions.

Raised when AI governance policies
block a request.
"""




class SecurityError(Exception):
    """
    Base security exception.
    """

    pass





class AIForbiddenError(SecurityError):
    """
    User is not allowed to access
    requested AI resource.
    """

    pass





class AIQuotaExceededError(SecurityError):
    """
    Token quota exceeded.
    """

    pass





class AIBudgetExceededError(SecurityError):
    """
    AI spending budget exceeded.
    """

    pass