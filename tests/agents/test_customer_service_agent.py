"""
Tests for CustomerServiceAgent.
"""

from __future__ import annotations


from datetime import datetime


import pytest


from app.agents.customer_service_agent import (
    CustomerServiceAgent,
)

from app.domain.customer.models import (
    Customer,
)

from app.domain.ticket.models import (
    Ticket,
    TicketPriority,
    TicketStatus,
)

from app.runtime.context import (
    AgentContext,
)



class FakeCustomerService:
    """
    Fake customer service.
    """

    async def get_customer(
        self,
        customer_id: str,
    ) -> Customer:

        return Customer(
            id=customer_id,
            name="Alice",
            email="alice@test.com",
            created_at=datetime.utcnow(),
        )



class FakeTicketService:
    """
    Fake ticket service.
    """

    def __init__(self) -> None:

        self.ticket = Ticket(
            id="ticket-001",
            customer_id="customer-001",
            title="Login issue",
            description="Cannot login",
            status=TicketStatus.OPEN,
            priority=TicketPriority.MEDIUM,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )


    async def get_ticket(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        if ticket_id == self.ticket.id:

            return self.ticket

        return None



    async def resolve_ticket(
        self,
        ticket_id: str,
    ) -> Ticket | None:

        if ticket_id == self.ticket.id:

            self.ticket.status = (
                TicketStatus.RESOLVED
            )

            return self.ticket

        return None



class FakeWorkflowResult:
    """
    Fake workflow execution result.
    """

    response = (
        "Ticket created successfully"
    )



class FakeWorkflow:
    """
    Fake workflow.
    """

    def build_graph(
        self,
    ):

        return "fake-graph"



class FakeWorkflowRegistry:
    """
    Fake workflow registry.
    """

    def get(
        self,
        name: str,
    ) -> FakeWorkflow:

        return FakeWorkflow()



class FakeWorkflowEngine:
    """
    Fake workflow engine.
    """

    async def execute(
        self,
        graph,
        state,
    ) -> FakeWorkflowResult:

        return FakeWorkflowResult()



def create_agent() -> CustomerServiceAgent:
    """
    Create test agent.
    """

    return CustomerServiceAgent(
        workflow_engine=(
            FakeWorkflowEngine()
        ),
        workflow_registry=(
            FakeWorkflowRegistry()
        ),
        customer_service=(
            FakeCustomerService()
        ),
        ticket_service=(
            FakeTicketService()
        ),
    )



@pytest.mark.asyncio
async def test_customer_service_agent_create_ticket():

    agent = create_agent()


    context = AgentContext(
        session_id="test-session",
        user_id="customer-001",
        input="My account has a problem",
    )


    result = await agent.execute(
        context
    )


    assert result.success is True


    assert (
        result.agent
        ==
        "customer_service_agent"
    )


    assert (
        result.metadata["type"]
        ==
        "ticket_workflow"
    )


    assert (
        result.response
        ==
        "Ticket created successfully"
    )



@pytest.mark.asyncio
async def test_customer_service_agent_greeting():

    agent = create_agent()


    context = AgentContext(
        session_id="test-session",
        user_id="customer-001",
        input="Hello",
    )


    result = await agent.execute(
        context
    )


    assert result.success is True


    assert (
        result.metadata["type"]
        ==
        "customer_support"
    )


    assert (
        "Alice"
        in result.response
    )



@pytest.mark.asyncio
async def test_customer_service_agent_query_ticket_status():

    agent = create_agent()


    context = AgentContext(
        session_id="test-session",
        user_id="customer-001",
        input="What is my ticket status?",
    )


    context.metadata = {
        "ticket_id": "ticket-001",
    }


    result = await agent.execute(
        context
    )


    assert result.success is True


    assert (
        result.metadata["type"]
        ==
        "ticket_status"
    )


    assert (
        "open"
        in result.response
    )



@pytest.mark.asyncio
async def test_customer_service_agent_resolve_ticket():

    agent = create_agent()


    context = AgentContext(
        session_id="test-session",
        user_id="customer-001",
        input="Please resolve my ticket",
    )


    context.metadata = {
        "ticket_id": "ticket-001",
    }


    result = await agent.execute(
        context
    )


    assert result.success is True


    assert (
        result.metadata["type"]
        ==
        "ticket_resolved"
    )


    assert (
        "Ticket resolved"
        in result.response
    )