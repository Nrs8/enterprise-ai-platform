"""
Conversation domain models.

Business conversation records.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime



@dataclass
class Conversation:
    """
    Customer conversation entity.
    """

    id: str

    customer_id: str

    session_id: str

    started_at: datetime

    ended_at: datetime | None = None