import logging

from app.task.executor import TaskExecutor
from app.task.queue import InMemoryTaskQueue


logger = logging.getLogger(__name__)


class TaskWorker:

    def __init__(
        self,
        task_queue: InMemoryTaskQueue,
        task_executor: TaskExecutor,
        worker_id: int,
    ) -> None:
        self._task_queue = task_queue
        self._task_executor = task_executor
        self._worker_id = worker_id

    async def run(self) -> None:


        while True:

            task_id = await self._task_queue.dequeue()


            logger.info(
                "Worker processing task",
                extra={
                    "worker_id": self._worker_id,
                    "task_id": task_id,
                },
            )
            trace = self._tracer.start_trace()
            try:
                with self._tracer.span(
                    trace,
                    "task_execution",
                    {
                        "worker_id": str(self._worker_id),
                        "task_id": task_id,
                    },
                ):
                    await self._task_executor.execute(
                        task_id=task_id,
                    )

            except Exception:

                logger.exception(
                    "Task execution failed",
                    extra={
                        "worker_id": self._worker_id,
                        "task_id": task_id,
                    },
                )

            finally:
                trace.finish()

                print(
                    "TASK TRACE:",
                    trace.trace_id,
                )

                for span in trace.spans:
                    print(
                        "SPAN:",
                        span.name,
                        span.attributes,
                    )

                self._task_queue.task_done()