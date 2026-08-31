"""
In-memory customer repository.

Development implementation.
"""

from __future__ import annotations

from app.domain.customer.models import Customer
from app.domain.customer.repository import CustomerRepository



class InMemoryCustomerRepository(CustomerRepository):
    """
    In-memory customer storage.
    """


    def __init__(self) -> None:

        self._customers: dict[str, Customer] = {}



    async def get(
        self,
        customer_id: str,
    ) -> Customer | None:

        return self._customers.get(
            customer_id
        )



    async def save(
        self,
        customer: Customer,
    ) -> None:

        self._customers[
            customer.id
        ] = customer