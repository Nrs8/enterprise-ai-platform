from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    session_id: str
    input: str
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None
    error: str | None = None