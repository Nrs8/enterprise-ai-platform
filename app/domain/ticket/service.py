"""
Ticket domain service.

Contains ticket business rules.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from .models import (
    Ticket,
    TicketPriority,
    TicketStatus,
)

from .repository import TicketRepository


class TicketService:
    """
    Ticket business operations.
    """

    def __init__(
        self,
        repository: TicketRepository,
    ) -> None:

        self.repository = repository


    async def create_ticket(
        self,
        customer_id: str,
        title: str,
        description: str,
        priority: TicketPriority = TicketPriority.MEDIUM,
    ) -> Ticket:
        """
        Create new support ticket.
        """

        now = datetime.utcnow()

        ticket = Ticket(
            id=str(uuid4()),
            customer_id=customer_id,
            title=title,
            description=description,
            status=TicketStatus.OPEN,
            priority=priority,
            created_at=now,
            updated_at=now,
        )

        await self.repository.save(
            ticket
        )

        return ticket


    async def get_ticket(
        self,
        ticket_id: str,
    ) -> Ticket | None:
        """
        Retrieve ticket by id.
        """

        return await (
            self.repository.get(
                ticket_id
            )
        )


    async def update_status(
        self,
        ticket_id: str,
        status: TicketStatus,
    ) -> Ticket | None:
        """
        Update ticket lifecycle status.
        """

        ticket = await self.get_ticket(
            ticket_id
        )

        if ticket is None:
            return None


        ticket.status = status

        ticket.updated_at = (
            datetime.utcnow()
        )


        await self.repository.save(
            ticket
        )


        return ticket


    async def resolve_ticket(
        self,
        ticket_id: str,
    ) -> Ticket | None:
        """
        Resolve support ticket.
        """

        return await self.update_status(
            ticket_id,
            TicketStatus.RESOLVED,
        )


    async def close_ticket(
        self,
        ticket_id: str,
    ) -> Ticket | None:
        """
        Close support ticket.
        """

        return await self.update_status(
            ticket_id,
            TicketStatus.CLOSED,
        )