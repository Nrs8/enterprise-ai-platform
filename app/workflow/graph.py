"""
Workflow graph operations.

Provides DAG management utilities:

- Node registration
- Edge registration
- Graph validation
- Topological sorting

The graph layer is responsible only for
workflow structure, not execution.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List

from app.workflow.models import (
    WorkflowEdge,
    WorkflowGraph,
    WorkflowNode,
)


class WorkflowGraphManager:
    """
    Manages workflow graph operations.

    Responsibilities:

    - Add nodes
    - Add edges
    - Validate graph
    - Generate execution order
    """

    def __init__(
        self,
        graph: WorkflowGraph | None = None,
    ) -> None:

        self.graph = graph or WorkflowGraph()


    # ========================================================
    # Node Operations
    # ========================================================

    def add_node(
        self,
        node: WorkflowNode,
    ) -> None:
        """
        Add a workflow node.
        """

        self.graph.add_node(node)


    # ========================================================
    # Edge Operations
    # ========================================================

    def add_edge(
        self,
        edge: WorkflowEdge,
    ) -> None:
        """
        Add a workflow edge.
        """

        self.graph.add_edge(edge)


    # ========================================================
    # DAG Validation
    # ========================================================

    def validate_dag(self) -> None:
        """
        Validate that workflow graph is a DAG.

        Raises:
            ValueError:
                If graph contains cycles.
        """

        self.topological_sort()


    # ========================================================
    # Topological Sort
    # ========================================================

    def topological_sort(
        self,
    ) -> List[str]:
        """
        Return execution order of nodes.

        Uses Kahn's algorithm.

        Example:

            A -> B -> C


        Returns:

            [
                "A",
                "B",
                "C"
            ]

        Raises:

            ValueError:
                If graph contains cycles.
        """

        nodes = self.graph.nodes

        edges = self.graph.edges


        # Calculate incoming edge count

        in_degree: Dict[str, int] = {
            node_id: 0
            for node_id in nodes
        }


        adjacency: Dict[str, List[str]] = defaultdict(
            list
        )


        for edge in edges:

            adjacency[
                edge.source
            ].append(
                edge.target
            )

            in_degree[
                edge.target
            ] += 1


        # Start with root nodes

        queue = deque(
            [
                node_id
                for node_id, degree in in_degree.items()
                if degree == 0
            ]
        )


        execution_order: List[str] = []


        while queue:

            node_id = queue.popleft()

            execution_order.append(
                node_id
            )


            for neighbor in adjacency[node_id]:

                in_degree[
                    neighbor
                ] -= 1


                if in_degree[neighbor] == 0:

                    queue.append(
                        neighbor
                    )


        # Cycle detection

        if len(execution_order) != len(nodes):

            raise ValueError(
                "Workflow graph contains cycle"
            )


        return execution_order


    # ========================================================
    # Query
    # ========================================================

    def get_node(
        self,
        node_id: str,
    ) -> WorkflowNode:
        """
        Get node by id.
        """

        if node_id not in self.graph.nodes:

            raise ValueError(
                f"Workflow node not found: {node_id}"
            )


        return self.graph.nodes[node_id]


    def get_graph(
        self,
    ) -> WorkflowGraph:
        """
        Return current graph.
        """

        return self.graph


__all__ = [
    "WorkflowGraphManager",
]