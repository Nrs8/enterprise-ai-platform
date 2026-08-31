"""
Customer domain models.

Business entities related to customers.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    """
    Customer entity.
    """

    id: str

    name: str

    email: str

    created_at: datetime