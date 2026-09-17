"""
Task API integration tests.
"""

from __future__ import annotations

from app.task.container import (
    task_manager,
)


async def fake_enqueue(
    task,
):
    return None


def test_create_task_propagates_identity(
    client,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.api.tasks.task_queue.enqueue",
        fake_enqueue,
    )

    response = client.post(
        "/tasks",
        json={
            "input": "What is 2 + 2?",
            "model": "qwen",
            "user_id": "enterprise_user",
            "tenant_id": "company_a",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["task_id"]
    assert body["session_id"]
    assert body["model"] == "qwen"
    assert body["status"] == "queued"

    task = task_manager.get_task(
        task_id=body["task_id"],
        user_id="enterprise_user",
        tenant_id="company_a",
    )

    assert task is not None
    assert task.input == "What is 2 + 2?"
    assert task.user_id == "enterprise_user"
    assert task.tenant_id == "company_a"


def test_get_task_enforces_ownership(
    client,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.api.tasks.task_queue.enqueue",
        fake_enqueue,
    )

    response = client.post(
        "/tasks",
        json={
            "input": "test task",
            "model": "qwen",
            "user_id": "enterprise_user",
            "tenant_id": "company_a",
        },
    )

    assert response.status_code == 200

    task_id = response.json()["task_id"]

    response = client.get(
        f"/tasks/{task_id}"
        "?user_id=enterprise_user"
        "&tenant_id=company_a"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["task_id"] == task_id

    response = client.get(
        f"/tasks/{task_id}"
        "?user_id=another_user"
        "&tenant_id=company_a"
    )

    assert response.status_code == 404

    response = client.get(
        f"/tasks/{task_id}"
        "?user_id=enterprise_user"
        "&tenant_id=another_tenant"
    )

    assert response.status_code == 404