"""
Workflow execution engine.

Responsible for executing workflow graphs.

Flow:

WorkflowGraph

    |

Topological Sort

    |

Execute Nodes

    |

WorkflowState
"""


from __future__ import annotations



import logging



from typing import Any, Dict



from app.workflow.graph import (
    WorkflowGraphManager,
)



from app.workflow.models import (
    WorkflowGraph,
    WorkflowState,
)






logger = logging.getLogger(
    __name__
)










class WorkflowNodeExecutor:
    """
    Base executor interface.

    Each workflow node type
    must provide an executor.
    """



    async def execute(

        self,

        state: WorkflowState,

    ) -> Dict[str, Any]:

        raise NotImplementedError











class WorkflowEngine:
    """
    Executes workflow DAG.

    Responsibilities:

    - Validate graph
    - Sort execution order
    - Execute nodes
    - Update workflow state


    Does NOT:

    - create plans
    - resolve agents
    - manage memory
    """





    def __init__(

        self,

    ) -> None:


        self.executors: Dict[

            str,

            WorkflowNodeExecutor,

        ] = {}









    def register_executor(

        self,

        node_type: str,

        executor: WorkflowNodeExecutor,

    ) -> None:
        """
        Register workflow node executor.
        """


        self.executors[

            node_type

        ] = executor










    async def execute(

        self,

        graph: WorkflowGraph,

        state: WorkflowState,

    ) -> WorkflowState:
        """
        Execute workflow graph.
        """



        manager = WorkflowGraphManager(

            graph

        )



        #
        # Validate DAG
        #

        manager.validate_dag()





        #
        # Execution order
        #

        execution_order = (

            manager.topological_sort()

        )




        logger.info(

            "Workflow execution order=%s",

            execution_order,

        )









        for node_id in execution_order:



            node = manager.get_node(

                node_id

            )



            state.current_node = (

                node_id

            )





            executor = (

                self.executors.get(

                    node.node_type

                )

            )





            if executor is None:


                raise RuntimeError(

                    "No executor registered "

                    f"for node type: {node.node_type}"

                )








            logger.info(

                "Executing workflow node=%s type=%s",

                node.name,

                node.node_type,

            )







            result = await executor.execute(

                state

            )





            state.add_result(

                node_id,

                result,

            )





            state.update(

                result

            )









        #
        # Final response
        #

        if "response" in state.variables:


            state.response = (

                state.variables["response"]

            )







        state.current_node = None





        return state