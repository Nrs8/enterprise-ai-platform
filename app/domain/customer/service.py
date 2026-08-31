"""
Customer domain service.

Contains customer business logic.
"""

from __future__ import annotations

from .models import Customer
from .repository import CustomerRepository


class CustomerService:
    """
    Customer business operations.
    """

    def __init__(
        self,
        repository: CustomerRepository,
    ) -> None:
        self.repository = repository


    async def get_customer(
        self,
        customer_id: str,
    ) -> Customer | None:
        """
        Get customer information.
        """

        return await self.repository.get(customer_id)