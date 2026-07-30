import asyncio

from fastapi import FastAPI

from app.api.chat import (
    task_executor,
    task_queue,
)

from app.api.chat import router as chat_router
from app.api.tasks import router as tasks_router
from app.task.worker import TaskWorker


app = FastAPI(
    title="Enterprise AI Platform"
)


app.include_router(chat_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def startup_event():


    worker_count = 3

    for worker_id in range(worker_count):

        worker = TaskWorker(
            task_queue=task_queue,
            task_executor=task_executor,
            worker_id=worker_id,
        )

        asyncio.create_task(
            worker.run()
        )