import asyncio

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.tasks import router as tasks_router
from app.api.health import router as health_router
from app.api.usage import router as usage_router

from app.container import Container

from app.task.container import (
    task_queue,
    task_manager,
)

from app.task.executor import TaskExecutor
from app.task.worker import TaskWorker

from app.observability.tracer import tracer


app = FastAPI(
    title="Enterprise AI Platform"
)


# =========================
# Register API routes
# =========================

app.include_router(chat_router)

app.include_router(usage_router)

app.include_router(tasks_router)

app.include_router(health_router)


# =========================
# Startup
# =========================

@app.on_event("startup")
async def startup_event():

    #
    # Create application container
    #

    app.state.container = Container()


    #
    # Create task executor
    #

    app.state.task_executor = TaskExecutor(

        task_manager=task_manager,

        agent_runtime=
            app.state.container.runtime,

    )


    #
    # Start workers
    #

    app.state.workers = []


    worker_count = 3


    for worker_id in range(worker_count):


        worker = TaskWorker(

            task_queue=task_queue,

            task_executor=
                app.state.task_executor,

            worker_id=worker_id,

            tracer=tracer,

        )


        app.state.workers.append(worker)


        asyncio.create_task(

            worker.run()

        )