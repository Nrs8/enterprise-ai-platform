"""
AI audit event models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AuditRecord:
    """
    Represents one AI governance audit event.
    """

    user_id: str
    tenant_id: str
    model: str
    action: str
    result: str
    reason: str
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)