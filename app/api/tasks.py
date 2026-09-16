"""
Task API endpoints.
"""

import logging
from uuid import uuid4

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from pydantic import BaseModel, Field

from app.task.container import (
    task_queue,
    task_manager,
)


logger = logging.getLogger(__name__)

router = APIRouter()


# =========================
# API Models
# =========================

class TaskRequest(BaseModel):
    """
    Async task request.
    """

    session_id: str | None = None

    input: str = Field(
        min_length=1,
        max_length=10000,
    )

    model: str = Field(
        default="qwen",
        min_length=1,
        max_length=100,
    )

    user_id: str = Field(
        default="anonymous",
        min_length=1,
        max_length=100,
    )

    tenant_id: str = Field(
        default="default",
        min_length=1,
        max_length=100,
    )


# =========================
# Create Task
# =========================

@router.post("/tasks")
async def create_task(
    http_request: Request,
    request: TaskRequest,
):
    """
    Create async Agent task.
    """

    container = (
        http_request
        .app
        .state
        .container
    )

    runtime = container.runtime

    if runtime is None:
        raise HTTPException(
            status_code=500,
            detail="AgentRuntime not initialized",
        )

    session_id = request.session_id

    if session_id is None:
        session_id = str(uuid4())

        container.memory_manager.create_conversation(
            session_id=session_id,
            user_id=request.user_id,
        )

    task = task_manager.create_task(
        session_id=session_id,
        input=request.input,
        model=request.model,
        user_id=request.user_id,
        tenant_id=request.tenant_id,
    )

    await task_queue.enqueue(
        task
    )

    logger.info(
        "Task submitted",
        extra={
            "task_id": task.id,
            "session_id": session_id,
            "model": request.model,
            "user_id": request.user_id,
            "tenant_id": request.tenant_id,
        },
    )

    return {
        "task_id": task.id,
        "session_id": session_id,
        "model": request.model,
        "status": "queued",
    }


# =========================
# Query Task
# =========================

@router.get("/tasks/{task_id}")
async def get_task(
    task_id: str,
    user_id: str = "anonymous",
    tenant_id: str = "default",
):
    """
    Get task status for the requested user and tenant.
    """

    task = task_manager.get_task(
        task_id=task_id,
        user_id=user_id,
        tenant_id=tenant_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "task_id": task.id,
        "session_id": task.session_id,
        "model": task.model,
        "status": task.status,
        "result": task.result,
        "error": task.error,
    }
