"""
Ticket workflow executors.

Provides node execution logic
for ticket workflows.
"""

from __future__ import annotations


from typing import Any, Dict


from app.workflow.engine import (
    WorkflowNodeExecutor,
)


from app.domain.ticket.service import (
    TicketService,
)


from app.domain.ticket.models import (
    TicketPriority,
)





class TicketValidationExecutor(
    WorkflowNodeExecutor
):
    """
    Validate ticket request.
    """



    async def execute(
        self,
        state,
    ) -> Dict[str, Any]:
        """
        Validate input data.
        """

        description = (
            state.variables.get(
                "description"
            )
        )


        if not description:

            raise ValueError(
                "Ticket description required"
            )


        return {

            "validated": True,

        }









class CreateTicketExecutor(
    WorkflowNodeExecutor
):
    """
    Create ticket through domain service.
    """



    def __init__(
        self,
        ticket_service: TicketService,
    ) -> None:

        self._ticket_service = (
            ticket_service
        )



    async def execute(
        self,
        state,
    ) -> Dict[str, Any]:
        """
        Create ticket entity.
        """

        ticket = await (
            self._ticket_service
            .create_ticket(
                customer_id=
                    state.variables[
                        "customer_id"
                    ],

                title=
                    state.variables[
                        "title"
                    ],

                description=
                    state.variables[
                        "description"
                    ],

                priority=
                    TicketPriority.MEDIUM,

            )
        )


        return {

            "ticket_id":
                ticket.id,

            "ticket_status":
                ticket.status.value,

        }









class TicketResponseExecutor(
    WorkflowNodeExecutor
):
    """
    Build workflow response.
    """



    async def execute(
        self,
        state,
    ) -> Dict[str, Any]:
        """
        Create final response.
        """

        ticket_id = (
            state.variables.get(
                "ticket_id"
            )
        )


        return {

            "response":
                (
                    "Ticket created successfully: "
                    f"{ticket_id}"
                )

        }