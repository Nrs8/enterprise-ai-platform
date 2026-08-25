"""
Workflow data models.

Defines workflow graph structures
and execution state.
"""


from __future__ import annotations


from dataclasses import dataclass, field


from typing import Any, Dict, List, Optional





# ============================================================
# Workflow Node
# ============================================================


@dataclass
class WorkflowNode:
    """
    Single executable workflow unit.
    """


    node_id: str


    name: str


    node_type: str


    metadata: Dict[str, Any] = field(
        default_factory=dict
    )









# ============================================================
# Workflow Edge
# ============================================================


@dataclass
class WorkflowEdge:
    """
    Directed workflow connection.
    """


    source: str


    target: str


    condition: Optional[str] = None









# ============================================================
# Workflow Graph
# ============================================================


@dataclass
class WorkflowGraph:
    """
    Workflow DAG graph.
    """


    nodes: Dict[str, WorkflowNode] = field(
        default_factory=dict
    )


    edges: List[WorkflowEdge] = field(
        default_factory=list
    )





    def add_node(

        self,

        node: WorkflowNode,

    ) -> None:


        if node.node_id in self.nodes:


            raise ValueError(

                f"Workflow node already exists: {node.node_id}"

            )


        self.nodes[node.node_id] = node







    def add_edge(

        self,

        edge: WorkflowEdge,

    ) -> None:


        if edge.source not in self.nodes:


            raise ValueError(

                f"Source node not found: {edge.source}"

            )


        if edge.target not in self.nodes:


            raise ValueError(

                f"Target node not found: {edge.target}"

            )


        self.edges.append(edge)









# ============================================================
# Workflow State
# ============================================================


@dataclass
class WorkflowState:
    """
    Runtime workflow execution state.


    Bridges:

        WorkflowEngine

             |

             v

        AgentContext

    """


    workflow_id: str



    session_id: Optional[str] = None



    current_node: Optional[str] = None



    variables: Dict[str, Any] = field(
        default_factory=dict
    )



    results: Dict[str, Any] = field(
        default_factory=dict
    )



    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



    response: Optional[str] = None





    def add_result(

        self,

        node_id: str,

        result: Dict[str, Any],

    ) -> None:


        self.results[node_id] = result





    def update(

        self,

        values: Dict[str, Any],

    ) -> None:


        self.variables.update(

            values

        )







__all__ = [

    "WorkflowNode",

    "WorkflowEdge",

    "WorkflowGraph",

    "WorkflowState",

]