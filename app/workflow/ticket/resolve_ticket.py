"""
Resolve ticket workflow definition.
"""

from __future__ import annotations


from app.workflow.models import (
    WorkflowGraph,
    WorkflowNode,
    WorkflowEdge,
)





class ResolveTicketWorkflow:
    """
    Ticket resolution workflow.
    """


    name = "resolve_ticket_workflow"



    def build_graph(
        self,
    ) -> WorkflowGraph:
        """
        Build resolve ticket graph.
        """

        graph = WorkflowGraph()



        graph.add_node(

            WorkflowNode(

                node_id="load_ticket",

                name="Load Ticket",

                node_type="service",

            )

        )



        graph.add_node(

            WorkflowNode(

                node_id="resolve_ticket",

                name="Resolve Ticket",

                node_type="service",

            )

        )



        graph.add_node(

            WorkflowNode(

                node_id="complete",

                name="Complete Resolution",

                node_type="response",

            )

        )



        graph.add_edge(

            WorkflowEdge(

                source="load_ticket",

                target="resolve_ticket",

            )

        )


        graph.add_edge(

            WorkflowEdge(

                source="resolve_ticket",

                target="complete",

            )

        )



        return graph