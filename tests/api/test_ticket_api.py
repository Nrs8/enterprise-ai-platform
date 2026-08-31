"""
Ticket API integration tests.
"""

from __future__ import annotations



def test_create_ticket(
    client,
):

    response = client.post(
        "/tickets",
        json={
            "customer_id": "customer-001",
            "title": "Login issue",
            "description": "Cannot login",
            "priority": "medium",
        },
    )


    assert response.status_code == 200


    body = response.json()


    assert body["customer_id"] == (
        "customer-001"
    )

    assert body["title"] == (
        "Login issue"
    )

    assert body["status"] == (
        "open"
    )

    assert body["priority"] == (
        "medium"
    )



def test_get_ticket_not_found(
    client,
):

    response = client.get(
        "/tickets/not-exist"
    )


    assert response.status_code == 404


    body = response.json()


    assert body["detail"] == (
        "Ticket not found"
    )



def test_update_ticket_invalid_status(
    client,
):

    response = client.patch(
        "/tickets/not-exist/status",
        json={
            "status": "invalid",
        },
    )


    assert response.status_code == 400


    body = response.json()


    assert body["detail"] == (
        "Invalid ticket status"
    )