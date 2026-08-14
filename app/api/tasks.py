"""
Task API endpoints.
"""


import logging


from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)


from pydantic import BaseModel


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

    input: str

    model: str = "qwen"



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


        session = (
            container
            .session_manager
            .create_session()
        )


        session_id = session.session_id



    task = task_manager.create_task(

        session_id=session_id,

        input=request.input,

        model=request.model,

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
):

    """
    Get task status.
    """


    task = task_manager.get_task(
        task_id
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