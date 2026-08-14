from app.task.queue import InMemoryTaskQueue
from app.task.manager import InMemoryTaskManager


task_queue = InMemoryTaskQueue()

task_manager = InMemoryTaskManager()