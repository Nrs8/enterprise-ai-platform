"""
Plan executor.

Responsible for converting execution plans
into workflow executions.

Architecture:

ExecutionPlan

    |

WorkflowBuilder

    |

WorkflowGraph

    |

WorkflowEngine

    |

WorkflowState
"""


from __future__ import annotations



from app.planning.models import (
    ExecutionPlan,
)



from app.planning.workflow_builder import (
    WorkflowBuilder,
)



from app.workflow.engine import (
    WorkflowEngine,
)



from app.workflow.models import (
    WorkflowState,
)







class PlanExecutor:
    """
    Executes planning results.

    Responsibilities:

    - Build workflow graph
    - Attach execution metadata
    - Delegate execution to WorkflowEngine


    Does NOT:

    - execute agents directly
    - call LLM
    - manage memory
    """







    def __init__(

        self,

        workflow_engine: WorkflowEngine,

        workflow_builder: WorkflowBuilder,

    ) -> None:



        self._workflow_engine = (
            workflow_engine
        )



        self._workflow_builder = (
            workflow_builder
        )









    async def execute(

        self,

        plan: ExecutionPlan,

        state: WorkflowState,

    ) -> WorkflowState:
        """
        Execute execution plan.


        Flow:


        Plan

          |

          v

        WorkflowGraph

          |

          v

        WorkflowEngine

          |

          v

        WorkflowState

        """



        #
        # Build workflow graph
        #

        graph = (

            self._workflow_builder

            .build(

                plan

            )

        )







        #
        # Store graph reference
        #
        # Workflow executors need
        # current node information.
        #

        state.metadata[

            "graph"

        ] = graph







        #
        # Execute workflow
        #

        result = await (

            self._workflow_engine

            .execute(

                graph,

                state,

            )

        )







        return result