import asyncio


class InMemoryTaskQueue:
    """
    In-memory asynchronous task queue.
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[str] = asyncio.Queue()

    async def enqueue(
        self,
        task_id: str,
    ) -> None:
        await self._queue.put(task_id)

    async def dequeue(self) -> str:
        return await self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()