import logging

from app.task.executor import TaskExecutor
from app.task.queue import InMemoryTaskQueue
from app.observability.metrics import metrics


logger = logging.getLogger(__name__)


class TaskWorker:

    def __init__(
        self,
        task_queue: InMemoryTaskQueue,
        task_executor: TaskExecutor,
        worker_id: int,
        tracer,
    ) -> None:
        self._task_queue = task_queue
        self._task_executor = task_executor
        self._worker_id = worker_id
        self._tracer = tracer


    async def run(self) -> None:

        while True:

            logger.info(
                "Worker waiting for task",
                extra={
                    "worker_id": self._worker_id,
                },
            )


            task = await self._task_queue.dequeue()


            logger.info(
                "Task received",
                extra={
                    "worker_id": self._worker_id,
                    "task_id": task.id,
                },
            )


            trace = self._tracer.start_trace()

            try:

                with self._tracer.span(
                    trace,
                    "task_execution",
                    {
                        "worker_id": str(self._worker_id),
                        "task_id": task.id,
                    },
                ):

                    await self._task_executor.execute(
                        task
                    )


                metrics.increment(
                    "tasks_processed"
                )


            except Exception:

                logger.exception(
                    "Task execution failed",
                    extra={
                        "worker_id": self._worker_id,
                        "task_id": task.id,
                    },
                )


                metrics.increment(
                    "tasks_failed"
                )

                raise


            finally:

                trace.finish()

                self._task_queue.task_done()