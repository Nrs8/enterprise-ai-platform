"""
Create ticket workflow definition.

Defines the workflow graph for
customer ticket creation.

Flow:

START
 |
 v
validate_request
 |
 v
create_ticket
 |
 v
complete
"""

from __future__ import annotations


from app.workflow.models import (
    WorkflowGraph,
    WorkflowNode,
    WorkflowEdge,
)





class CreateTicketWorkflow:
    """
    Ticket creation workflow.

    Responsible for defining workflow structure.

    Execution is handled by WorkflowEngine.
    """


    name = "create_ticket_workflow"



    def build_graph(
        self,
    ) -> WorkflowGraph:
        """
        Build ticket creation workflow graph.
        """

        graph = WorkflowGraph()



        #
        # Nodes
        #

        graph.add_node(

            WorkflowNode(

                node_id="validate_request",

                name="Validate Ticket Request",

                node_type="validation",

                metadata={

                    "description":
                        "Validate customer ticket input",

                },

            )

        )



        graph.add_node(

            WorkflowNode(

                node_id="create_ticket",

                name="Create Ticket",

                node_type="service",

                metadata={

                    "service":
                        "TicketService",

                },

            )

        )



        graph.add_node(

            WorkflowNode(

                node_id="complete",

                name="Complete Ticket Creation",

                node_type="response",

                metadata={

                    "description":
                        "Return ticket result",

                },

            )

        )





        #
        # Edges
        #

        graph.add_edge(

            WorkflowEdge(

                source="validate_request",

                target="create_ticket",

            )

        )


        graph.add_edge(

            WorkflowEdge(

                source="create_ticket",

                target="complete",

            )

        )



        return graph