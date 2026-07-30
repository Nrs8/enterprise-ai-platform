from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.api.chat import (
    session_manager,
    task_manager,
    task_executor,
)


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


class TaskRequest(BaseModel):
    session_id: str | None = None
    message: str


async def execute_task(task_id: str) -> None:
    """
    Execute a task in the background.
    """

    await task_executor.execute(
        task_id=task_id,
    )


@router.post("")
async def create_task(
    request: TaskRequest,
    background_tasks: BackgroundTasks,
):
    """
    Create a task and execute it in the background.
    """

    session_id = request.session_id

    if session_id is None:
        session = session_manager.create_session()
        session_id = session.session_id

    task = task_manager.create_task(
        session_id=session_id,
        input=request.message,
    )

    background_tasks.add_task(
        execute_task,
        task.id,
    )

    return {
        "task_id": task.id,
        "session_id": session_id,
        "status": task.status,
    }


@router.get("/{task_id}")
async def get_task(task_id: str):
    """
    Get the current task state.
    """

    task = task_manager.get_task(
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "task_id": task.id,
        "session_id": task.session_id,
        "status": task.status,
        "result": task.result,
        "error": task.error,
    }