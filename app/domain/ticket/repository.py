"""
Ticket repository abstraction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Ticket


class TicketRepository(ABC):
    """
    Ticket persistence contract.
    """

    @abstractmethod
    async def get(
        self,
        ticket_id: str,
    ) -> Ticket | None:
        """
        Retrieve ticket by id.
        """
        ...


    @abstractmethod
    async def save(
        self,
        ticket: Ticket,
    ) -> None:
        """
        Persist ticket.
        """
        ...


    @abstractmethod
    async def list_by_customer(
        self,
        customer_id: str,
    ) -> list[Ticket]:
        """
        Retrieve tickets belonging to a customer.
        """
        ...