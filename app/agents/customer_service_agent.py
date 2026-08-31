"""
Customer Service Agent.

Responsible for customer support workflows.
"""

from __future__ import annotations

import logging

from app.agents.base import BaseAgent
from app.agents.models import AgentResult

from app.domain.customer.service import CustomerService
from app.domain.ticket.service import TicketService

from app.runtime.context import AgentContext

from app.workflow.engine import WorkflowEngine
from app.workflow.registry import WorkflowRegistry
from app.workflow.state import WorkflowState


logger = logging.getLogger(
    "app.agents.customer_service_agent"
)


class CustomerServiceAgent(BaseAgent):
    """
    Agent responsible for customer support operations.

    Flow:

        AgentContext
             |
             v
        CustomerServiceAgent
             |
             +----------------+
             |                |
             v                v
    CustomerService     TicketService

             |

             v

       WorkflowEngine

             |

             v

    create_ticket_workflow

             |

             v

        AgentResult
    """

    name = "customer_service_agent"


    def __init__(
        self,
        workflow_engine: WorkflowEngine,
        workflow_registry: WorkflowRegistry,
        customer_service: CustomerService,
        ticket_service: TicketService,
    ) -> None:
        """
        Initialize customer service agent.
        """

        self._workflow_engine = (
            workflow_engine
        )

        self._workflow_registry = (
            workflow_registry
        )

        self._customer_service = (
            customer_service
        )

        self._ticket_service = (
            ticket_service
        )


    async def execute(
        self,
        context: AgentContext,
    ) -> AgentResult:
        """
        Execute customer support workflow.
        """

        logger.info(
            "CustomerServiceAgent executing"
        )


        try:

            request = (
                context.input.lower()
            )


            customer = None


            if context.user_id:

                customer = await (
                    self._customer_service
                    .get_customer(
                        context.user_id
                    )
                )


            #
            # Ticket status query
            #

            if (
                "status" in request
                or "state" in request
            ):

                ticket_id = (
                    context.metadata
                    .get(
                        "ticket_id"
                    )
                    if context.metadata
                    else None
                )


                if ticket_id:

                    ticket = await (
                        self._ticket_service
                        .get_ticket(
                            ticket_id
                        )
                    )


                    if ticket:

                        response = (
                            "Ticket status: "
                            f"{ticket.status.value}"
                        )


                        context.set_response(
                            response
                        )


                        return AgentResult(
                            response=response,
                            success=True,
                            agent=self.name,
                            metadata={
                                "type":
                                "ticket_status",
                            },
                        )



            #
            # Resolve ticket
            #

            if (
                "resolve" in request
                or "close" in request
            ):

                ticket_id = (
                    context.metadata
                    .get(
                        "ticket_id"
                    )
                    if context.metadata
                    else None
                )


                if ticket_id:

                    ticket = await (
                        self._ticket_service
                        .resolve_ticket(
                            ticket_id
                        )
                    )


                    if ticket:

                        response = (
                            "Ticket resolved: "
                            f"{ticket.id}"
                        )


                        context.set_response(
                            response
                        )


                        return AgentResult(
                            response=response,
                            success=True,
                            agent=self.name,
                            metadata={
                                "type":
                                "ticket_resolved",
                            },
                        )



            #
            # Ticket creation workflow
            #

            if (
                "ticket" in request
                or "problem" in request
                or "issue" in request
                or "error" in request
                or "failed" in request
            ):


                result = await (
                    self._execute_ticket_workflow(
                        context,
                        customer,
                    )
                )


                response = (
                    result.response
                    or "Ticket created"
                )


                context.set_response(
                    response
                )


                return AgentResult(
                    response=response,
                    success=True,
                    agent=self.name,
                    metadata={
                        "type":
                        "ticket_workflow",

                        "workflow":
                        (
                            "create_ticket_workflow"
                        ),
                    },
                )



            #
            # Customer lookup response
            #

            if customer:

                response = (
                    f"Hello {customer.name}, "
                    "how can I assist you today?"
                )

            else:

                response = (
                    "How can I assist you today?"
                )


            context.set_response(
                response
            )


            return AgentResult(
                response=response,
                success=True,
                agent=self.name,
                metadata={
                    "type":
                    "customer_support",
                },
            )


        except Exception as exc:

            logger.exception(
                "CustomerServiceAgent failed"
            )


            return AgentResult(
                response=(
                    "Customer service request failed"
                ),
                success=False,
                agent=self.name,
                error=str(exc),
            )



    async def _execute_ticket_workflow(
        self,
        context: AgentContext,
        customer=None,
    ):
        """
        Execute ticket creation workflow.
        """

        workflow = (
            self._workflow_registry
            .get(
                "create_ticket_workflow"
            )
        )


        graph = (
            workflow.build_graph()
        )


        state = WorkflowState(

            workflow_id=(
                "create_ticket_workflow"
            ),

            session_id=
                context.session_id,

        )


        state.update(
            {
                "customer_id":
                    context.user_id,

                "customer":
                    customer,

                "title":
                    (
                        "Customer support request"
                    ),

                "description":
                    context.input,
            }
        )


        return await (
            self._workflow_engine
            .execute(
                graph,
                state,
            )
        )