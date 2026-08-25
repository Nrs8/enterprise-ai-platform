"""
Workflow builder.

Converts ExecutionPlan
into WorkflowGraph.
"""


from __future__ import annotations


from app.planning.models import (
    ExecutionPlan,
)


from app.workflow.models import (
    WorkflowGraph,
    WorkflowNode,
    WorkflowEdge,
)





class WorkflowBuilder:
    """
    Convert execution plan
    into workflow DAG.
    """



    def build(

        self,

        plan: ExecutionPlan,

    ) -> WorkflowGraph:
        """
        Build workflow graph.

        PlanStep.name becomes
        WorkflowNode.node_id.
        """


        graph = WorkflowGraph()



        previous_node_id = None



        for step in plan.steps:



            #
            # Stable node identity
            #

            node_id = step.name





            node = WorkflowNode(

                node_id=node_id,

                name=step.name,

                node_type=step.task_type.value,

                metadata={

                    #
                    # Test contract
                    #

                    "task":
                        step.description,


                    #
                    # Runtime information
                    #

                    "description":
                        step.description,


                    "input":
                        step.input,


                    "task_type":
                        step.task_type.value,

                },

            )





            graph.add_node(

                node

            )







            #
            # Sequential dependency
            #

            if previous_node_id:



                graph.add_edge(

                    WorkflowEdge(

                        source=previous_node_id,

                        target=node_id,

                    )

                )





            previous_node_id = node_id





        return graph