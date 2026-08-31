"""
Ticket API endpoints.
"""

from __future__ import annotations


from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)


from pydantic import BaseModel


from app.domain.ticket.models import (
    TicketPriority,
)



router = APIRouter()



class CreateTicketRequest(BaseModel):
    """
    Create ticket payload.
    """

    customer_id: str

    title: str

    description: str

    priority: TicketPriority = (
        TicketPriority.MEDIUM
    )



@router.post("/tickets")
async def create_ticket(
    http_request: Request,
    request: CreateTicketRequest,
):
    """
    Create customer ticket.
    """

    container = (
        http_request
        .app
        .state
        .container
    )


    ticket = await (
        container.ticket_service
        .create_ticket(
            customer_id=request.customer_id,
            title=request.title,
            description=request.description,
            priority=request.priority,
        )
    )


    return {
        "id": ticket.id,
        "customer_id": ticket.customer_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": (
            ticket.status.value
        ),
        "priority": (
            ticket.priority.value
        ),
    }



@router.get("/tickets/{ticket_id}")
async def get_ticket(
    http_request: Request,
    ticket_id: str,
):
    """
    Get ticket information.
    """

    container = (
        http_request
        .app
        .state
        .container
    )


    ticket = await (
        container.ticket_service
        .get_ticket(
            ticket_id
        )
    )


    if ticket is None:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )


    return {
        "id": ticket.id,
        "customer_id": ticket.customer_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": (
            ticket.status.value
        ),
        "priority": (
            ticket.priority.value
        ),
    }



class UpdateTicketStatusRequest(BaseModel):
    """
    Update ticket status payload.
    """

    status: str



@router.patch("/tickets/{ticket_id}/status")
async def update_ticket_status(
    http_request: Request,
    ticket_id: str,
    request: UpdateTicketStatusRequest,
):
    """
    Update ticket lifecycle state.
    """

    from app.domain.ticket.models import (
        TicketStatus,
    )


    container = (
        http_request
        .app
        .state
        .container
    )


    try:

        status = TicketStatus(
            request.status
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status",
        )


    ticket = await (
        container.ticket_service
        .update_status(
            ticket_id,
            status,
        )
    )


    if ticket is None:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )


    return {
        "id": ticket.id,
        "status": (
            ticket.status.value
        ),
    }