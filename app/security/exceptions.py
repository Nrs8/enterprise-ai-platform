"""
Security and governance exceptions.

Raised when AI governance policies
block a request.
"""

from app.runtime.errors.exceptions import (
    AuthorizationError,
)


class SecurityError(AuthorizationError):
    """
    Base security exception.
    """

    pass


class AIForbiddenError(SecurityError):
    """
    User is not allowed to access
    requested AI resource.
    """

    code = "ai_forbidden"


class AIQuotaExceededError(SecurityError):
    """
    Token quota exceeded.
    """

    code = "ai_quota_exceeded"


class AIBudgetExceededError(SecurityError):
    """
    AI spending budget exceeded.
    """

    code = "ai_budget_exceeded"