"""
Customer API integration tests.
"""

from __future__ import annotations



def test_get_customer_not_found(
    client,
):

    response = client.get(
        "/customers/not-exist"
    )


    assert response.status_code == 404


    body = response.json()


    assert body["detail"] == (
        "Customer not found"
    )