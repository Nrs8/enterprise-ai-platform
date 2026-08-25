"""
Planning domain models.

Defines planning tasks,
execution steps,
workflow compatible plans.
"""


from __future__ import annotations


from dataclasses import dataclass, field


from enum import Enum


from typing import Any, Dict, List





# ============================================================
# Task Type
# ============================================================


class TaskType(str, Enum):
    """
    Task classification.
    """


    GENERAL = "general"


    KNOWLEDGE = "knowledge"


    TOOL = "tool"









# ============================================================
# Task
# ============================================================


@dataclass
class Task:
    """
    User task description.

    Planner input abstraction.
    """


    description: str


    task_type: TaskType = (
        TaskType.GENERAL
    )









# ============================================================
# Workflow Plan Step
# ============================================================


@dataclass
class PlanStep:
    """
    One executable workflow step.

    Planner creates this object.

    WorkflowBuilder converts it
    into workflow nodes.

    Planner does NOT know agents.
    """


    name: str


    task_type: TaskType


    description: str = ""


    input: Dict[str, Any] = field(
        default_factory=dict
    )









# ============================================================
# Execution Plan
# ============================================================


@dataclass
class ExecutionPlan:
    """
    Complete execution plan.

    Produced by Planner.

    Consumed by WorkflowBuilder.
    """


    steps: List[PlanStep] = field(
        default_factory=list
    )


    metadata: Dict[str, Any] = field(
        default_factory=dict
    )








# ============================================================
# Plan Result
# ============================================================


@dataclass
class PlanResult:
    """
    Result after plan execution.
    """


    response: str


    steps_completed: int = 0


    metadata: Dict[str, Any] = field(
        default_factory=dict
    )








__all__ = [

    "TaskType",

    "Task",

    "PlanStep",

    "ExecutionPlan",

    "PlanResult",

]