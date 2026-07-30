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
    ) -> Task:
        task = Task(
            id=str(uuid4()),
            session_id=session_id,
            input=input,
        )

        self._tasks[task.id] = task

        return task

    def get_task(
        self,
        task_id: str,
    ) -> Task | None:
        return self._tasks.get(task_id)

    def update_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: str | None = None,
        error: str | None = None,
    ) -> Task | None:
        task = self._tasks.get(task_id)

        if task is None:
            return None

        task.status = status

        if result is not None:
            task.result = result

        if error is not None:
            task.error = error

        return task