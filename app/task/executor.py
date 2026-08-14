from app.runtime.runtime import AgentRuntime
from app.task.manager import InMemoryTaskManager
from app.task.models import Task, TaskStatus


class TaskExecutor:
    """
    Executes tasks through the AgentRuntime.
    """


    def __init__(
        self,
        task_manager: InMemoryTaskManager,
        agent_runtime: AgentRuntime,
    ) -> None:

        self._task_manager = task_manager

        self._agent_runtime = agent_runtime



    async def execute(
        self,
        task: Task,
    ):

        """
        Execute a task object.
        """


        self._task_manager.update_status(
            task_id=task.id,
            status=TaskStatus.RUNNING,
        )


        try:


            result = await self._agent_runtime.chat(

                session_id=task.session_id,

                message=task.input,

                model=task.model,

            )


            self._task_manager.update_status(

                task_id=task.id,

                status=TaskStatus.COMPLETED,

                result=result,

            )


            return result



        except Exception as exc:


            self._task_manager.update_status(

                task_id=task.id,

                status=TaskStatus.FAILED,

                error=str(exc),

            )


            raise