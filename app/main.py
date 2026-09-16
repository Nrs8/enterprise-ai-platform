"""
Enterprise AI Platform application entry point.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.audit import (
    router as audit_router,
)
from app.api.chat import (
    router as chat_router,
)
from app.api.customers import (
    router as customers_router,
)
from app.api.error_handler import (
    runtime_exception_handler,
)
from app.api.health import (
    router as health_router,
)
from app.api.tasks import (
    router as tasks_router,
)
from app.api.tickets import (
    router as tickets_router,
)
from app.api.usage import (
    router as usage_router,
)
from app.config import settings
from app.container import (
    Container,
)
from app.observability.tracer import (
    tracer,
)
from app.runtime.errors import (
    RuntimeErrorBase,
)
from app.task.container import (
    task_manager,
    task_queue,
)
from app.task.executor import (
    TaskExecutor,
)
from app.task.worker import (
    TaskWorker,
)


@asynccontextmanager
async def lifespan(
    application: FastAPI,
) -> AsyncIterator[None]:
    """
    Initialize and manage application services.
    """

    #
    # Create application container
    #

    application.state.container = Container()

    #
    # Create task executor
    #

    application.state.task_executor = TaskExecutor(
        task_manager=task_manager,
        agent_runtime=application.state.container.runtime,
    )

    #
    # Start background workers
    #

    application.state.workers = []
    application.state.worker_tasks = []

    worker_count = settings.worker_count

    for worker_id in range(worker_count):
        worker = TaskWorker(
            task_queue=task_queue,
            task_executor=application.state.task_executor,
            worker_id=worker_id,
            tracer=tracer,
        )

        application.state.workers.append(worker)

        worker_task = asyncio.create_task(
            worker.run()
        )

        application.state.worker_tasks.append(
            worker_task
        )

    try:
        yield

    finally:
        #
        # Stop background workers
        #

        for worker_task in application.state.worker_tasks:
            worker_task.cancel()

        await asyncio.gather(
            *application.state.worker_tasks,
            return_exceptions=True,
        )


app = FastAPI(
    title="Enterprise AI Platform",
    lifespan=lifespan,
)


# =========================
# Register exception handlers
# =========================

app.add_exception_handler(
    RuntimeErrorBase,
    runtime_exception_handler,
)


# =========================
# Register API routes
# =========================

app.include_router(
    chat_router
)

app.include_router(
    usage_router
)

app.include_router(
    tasks_router
)

app.include_router(
    health_router
)

app.include_router(
    customers_router
)

app.include_router(
    tickets_router
)

app.include_router(
    audit_router
)
