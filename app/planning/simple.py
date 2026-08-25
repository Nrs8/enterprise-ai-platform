"""
Simple rule based planner.

First implementation of Planner.

Later replaced by LLM based planner.
"""


import uuid


from app.planning.base import Planner


from app.planning.models import (
    Plan,
    Task,
    TaskType,
    ExecutionStep,
)



class SimplePlanner(Planner):
    """
    Rule based planning engine.

    Converts user request into
    simple execution steps.
    """



    async def create_plan(
        self,
        context,
    ) -> Plan:
        """
        Create execution plan.
        """


        user_input = (
            context.input.lower()
        )


        task_type = TaskType.GENERAL


        if any(
            keyword in user_input
            for keyword in [
                "calculate",
                "compute",
                "sum",
                "multiply",
                "+",
                "*",
            ]
        ):

            task_type = TaskType.TOOL


        elif any(
            keyword in user_input
            for keyword in [
                "document",
                "policy",
                "knowledge",
                "information",
            ]
        ):

            task_type = TaskType.KNOWLEDGE



        task = Task(

            description=context.input,

            task_type=task_type,

        )



        plan = Plan(

            task=task,

        )



        if task_type == TaskType.TOOL:


            plan.add_step(

                ExecutionStep(

                    id=str(
                        uuid.uuid4()
                    ),

                    agent="tool_agent",

                    task=(
                        "Execute required tool"
                    ),

                )

            )


        elif task_type == TaskType.KNOWLEDGE:


            plan.add_step(

                ExecutionStep(

                    id=str(
                        uuid.uuid4()
                    ),

                    agent="knowledge_agent",

                    task=(
                        "Retrieve relevant knowledge"
                    ),

                )

            )


        else:


            plan.add_step(

                ExecutionStep(

                    id=str(
                        uuid.uuid4()
                    ),

                    agent="tool_agent",

                    task=(
                        "Handle general request"
                    ),

                )

            )


        return plan