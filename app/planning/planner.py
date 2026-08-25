"""
Default rule based planner.

Later can be replaced by:

- LLM Planner
- ReAct Planner
- Tree Search Planner
"""


from __future__ import annotations


import logging



from app.planning.base import Planner


from app.planning.models import (
    ExecutionPlan,
    PlanStep,
    TaskType,
)


from app.runtime.context import AgentContext





logger = logging.getLogger(
    "app.planning"
)








class SimplePlanner(Planner):
    """
    Deterministic rule based planner.

    Planner decides:

    WHAT needs to happen.

    It does NOT decide:

    WHICH AGENT executes it.
    """





    async def create_plan(

        self,

        context: AgentContext,

    ) -> ExecutionPlan:
        """
        Generate execution workflow.
        """



        message = (

            context.input.lower()

        )



        steps: list[PlanStep] = []





        #
        # Tool task
        #

        if any(

            keyword in message

            for keyword in [

                "calculate",

                "compute",

                "+",

                "-",

                "*",

                "/",

                "sum",

            ]

        ):


            steps.append(

                PlanStep(

                    name="tool_execution",

                    task_type=TaskType.TOOL,

                    description=(

                        "Execute calculation task"

                    ),

                )

            )





        #
        # Knowledge task
        #

        else:


            steps.append(

                PlanStep(

                    name="knowledge_answer",

                    task_type=TaskType.KNOWLEDGE,

                    description=(

                        "Retrieve knowledge and answer"

                    ),

                )

            )








        plan = ExecutionPlan(

            steps=steps,

            metadata={

                "planner":

                    "simple_planner",

            },

        )





        logger.info(

            "Created execution plan steps=%s",

            len(

                plan.steps

            ),

        )





        return plan