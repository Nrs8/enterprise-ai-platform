"""
Chat API integration tests.
"""

from __future__ import annotations


class FakeRuntime:

    def __init__(self):
        self.calls = []

    async def chat(
        self,
        session_id,
        message,
        model,
        user_id,
        tenant_id,
    ):
        self.calls.append(
            {
                "session_id": session_id,
                "message": message,
                "model": model,
                "user_id": user_id,
                "tenant_id": tenant_id,
            }
        )

        return "fake response"


def test_chat_propagates_identity(
    client,
):
    runtime = client.app.state.container.runtime

    fake_runtime = FakeRuntime()

    client.app.state.container.runtime = (
        fake_runtime
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "model": "qwen",
            "user_id": "enterprise_user",
            "tenant_id": "company_a",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["model"] == "qwen"
    assert body["response"] == "fake response"
    assert body["session_id"]

    assert len(fake_runtime.calls) == 1

    call = fake_runtime.calls[0]

    assert call["message"] == "Hello"
    assert call["model"] == "qwen"
    assert call["user_id"] == "enterprise_user"
    assert call["tenant_id"] == "company_a"

    client.app.state.container.runtime = runtime


def test_chat_rejects_empty_message(
    client,
):
    response = client.post(
        "/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422