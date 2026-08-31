"""
Ticket domain models.

Customer support ticket entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TicketStatus(str, Enum):
    """
    Ticket lifecycle states.
    """

    OPEN = "open"

    ASSIGNED = "assigned"

    IN_PROGRESS = "in_progress"

    WAITING_CUSTOMER = "waiting_customer"

    RESOLVED = "resolved"

    CLOSED = "closed"



class TicketPriority(str, Enum):
    """
    Ticket priority levels.
    """

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"



@dataclass
class Ticket:
    """
    Customer support ticket entity.
    """

    id: str

    customer_id: str

    title: str

    description: str

    status: TicketStatus

    priority: TicketPriority

    created_at: datetime

    updated_at: datetime