"""
Tests for TicketService.
"""

from __future__ import annotations


import pytest


from app.domain.ticket.models import (
    TicketStatus,
)

from app.domain.ticket.service import (
    TicketService,
)



class FakeTicketRepository:
    """
    Fake ticket repository.
    """

    def __init__(self) -> None:

        self.tickets = {}


    async def save(
        self,
        ticket,
    ) -> None:

        self.tickets[ticket.id] = ticket


    async def get(
        self,
        ticket_id: str,
    ):

        return self.tickets.get(
            ticket_id
        )



@pytest.mark.asyncio
async def test_create_ticket():

    repository = FakeTicketRepository()

    service = TicketService(
        repository
    )


    ticket = await service.create_ticket(
        customer_id="customer-001",
        title="Login problem",
        description="Cannot login",
    )


    assert ticket.customer_id == "customer-001"

    assert (
        ticket.status
        ==
        TicketStatus.OPEN
    )

    assert (
        repository.tickets[ticket.id]
        ==
        ticket
    )



@pytest.mark.asyncio
async def test_resolve_ticket():

    repository = FakeTicketRepository()

    service = TicketService(
        repository
    )


    ticket = await service.create_ticket(
        customer_id="customer-001",
        title="Login problem",
        description="Cannot login",
    )


    updated = await service.resolve_ticket(
        ticket.id
    )


    assert updated is not None

    assert (
        updated.status
        ==
        TicketStatus.RESOLVED
    )



@pytest.mark.asyncio
async def test_close_ticket():

    repository = FakeTicketRepository()

    service = TicketService(
        repository
    )


    ticket = await service.create_ticket(
        customer_id="customer-001",
        title="Payment issue",
        description="Payment failed",
    )


    updated = await service.close_ticket(
        ticket.id
    )


    assert updated is not None

    assert (
        updated.status
        ==
        TicketStatus.CLOSED
    )