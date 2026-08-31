"""
Customer API endpoints.
"""

from __future__ import annotations


from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)


router = APIRouter()



@router.get("/customers/{customer_id}")
async def get_customer(
    http_request: Request,
    customer_id: str,
):
    """
    Get customer information.
    """

    container = (
        http_request
        .app
        .state
        .container
    )


    customer = await (
        container.customer_service
        .get_customer(
            customer_id
        )
    )


    if customer is None:

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )


    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "created_at": (
            customer.created_at
        ),
    }