"""
In-memory task lifecycle manager.
"""

from uuid import uuid4

from app.task.models import Task, TaskStatus


class InMemoryTaskManager:
    """
    In-memory task lifecycle manager.
    """

    def __init__(self) -> None:

        self._tasks: dict[str, Task] = {}

    def create_task(
        self,
        session_id: str,
        input: str,
        model: str = "qwen",
        user_id: str = "anonymous",
        tenant_id: str = "default",
    ) -> Task:
        """
        Create new async task.
        """

        task = Task(
            id=str(uuid4()),
            session_id=session_id,
            input=input,
            model=model,
            user_id=user_id,
            tenant_id=tenant_id,
            status=TaskStatus.PENDING,
        )

        self._tasks[task.id] = task

        return task

    def get_task(
        self,
        task_id: str,
        user_id: str = "anonymous",
        tenant_id: str = "default",
    ) -> Task | None:
        """
        Get task by id if it belongs to the requested user and tenant.
        """

        task = self._tasks.get(task_id)

        if task is None:
            return None

        if task.user_id != user_id:
            return None

        if task.tenant_id != tenant_id:
            return None

        return task

    def update_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: str | None = None,
        error: str | None = None,
    ) -> Task | None:
        """
        Update task status.
        """

        task = self._tasks.get(task_id)

        if task is None:
            return None

        task.status = status

        if result is not None:
            task.result = result

        if error is not None:
            task.error = error

        return task
