"""
Customer repository abstraction.

Defines persistence contract for customer domain.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Customer


class CustomerRepository(ABC):
    """
    Customer persistence contract.
    """


    @abstractmethod
    async def get(
        self,
        customer_id: str,
    ) -> Customer | None:
        """
        Retrieve customer by id.
        """
        ...


    @abstractmethod
    async def save(
        self,
        customer: Customer,
    ) -> None:
        """
        Persist customer.
        """
        ...