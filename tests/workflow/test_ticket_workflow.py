"""
Ticket workflow tests.

Tests customer ticket creation workflow graph.
"""

import pytest


from app.workflow.ticket import (
    CreateTicketWorkflow,
)



@pytest.mark.asyncio
async def test_create_ticket_workflow():

    workflow = CreateTicketWorkflow()


    graph = workflow.build_graph()


    assert (
        "validate_request"
        in graph.nodes
    )


    assert (
        "create_ticket"
        in graph.nodes
    )


    assert (
        "complete"
        in graph.nodes
    )


    assert len(
        graph.edges
    ) == 2