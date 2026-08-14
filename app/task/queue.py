import asyncio

from app.task.models import Task


class InMemoryTaskQueue:
    """
    In-memory asynchronous task queue.
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[Task] = asyncio.Queue()


    async def enqueue(
        self,
        task: Task,
    ) -> None:

        await self._queue.put(task)


    async def dequeue(self) -> Task:

        return await self._queue.get()


    def task_done(self) -> None:

        self._queue.task_done()