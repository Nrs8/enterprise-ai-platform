"""
In-memory ticket repository.

Development implementation.
"""

from __future__ import annotations


from app.domain.ticket.models import Ticket
from app.domain.ticket.repository import TicketRepository



class InMemoryTicketRepository(
    TicketRepository
):
    """
    In-memory ticket storage.
    """


    def __init__(self) -> None:

        self._tickets: dict[str, Ticket] = {}



    async def get(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        return self._tickets.get(
            ticket_id
        )



    async def save(
        self,
        ticket: Ticket,
    ) -> None:

        self._tickets[
            ticket.id
        ] = ticket



    async def list_by_customer(
        self,
        customer_id: str,
    ) -> list[Ticket]:

        return [

            ticket

            for ticket in self._tickets.values()

            if ticket.customer_id == customer_id

        ]