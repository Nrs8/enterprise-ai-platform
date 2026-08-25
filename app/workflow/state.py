"""
Workflow runtime state management.

Responsible for maintaining workflow execution state.

Supports:

- State updates
- State merging
- Snapshot creation
- Future persistence/checkpoint extension
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class WorkflowState:
    """
    Runtime state of a workflow execution.

    The state is shared between workflow nodes.

    Example:

        RetrieveNode

            updates

        retrieved_documents


        ToolNode

            updates

        tool_result


        LLMNode

            updates

        answer
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
    response: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )


    # ========================================================
    # Update Operations
    # ========================================================

    def update(
        self,
        values: Dict[str, Any],
    ) -> None:
        """
        Update workflow variables.

        Example:

            state.update(
                {
                    "answer": "hello"
                }
            )
        """

        self.variables.update(
            values
        )

        self.updated_at = (
            datetime.utcnow()
        )


    def add_result(
        self,
        node_id: str,
        result: Dict[str, Any],
    ) -> None:
        """
        Store node execution result.

        Example:

            {
                "retrieve":
                    {
                        "documents": []
                    }
            }
        """

        self.results[
            node_id
        ] = result


        self.updated_at = (
            datetime.utcnow()
        )


    # ========================================================
    # Snapshot
    # ========================================================

    def snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Create serializable workflow snapshot.

        Used for:

        - persistence
        - checkpoint
        - recovery
        """

        return {
            "workflow_id": self.workflow_id,

            "session_id": self.session_id,

            "current_node": self.current_node,

            "variables": self.variables.copy(),

            "results": self.results.copy(),

            "metadata": self.metadata.copy(),

            "created_at": (
                self.created_at.isoformat()
            ),

            "updated_at": (
                self.updated_at.isoformat()
            ),
        }


    # ========================================================
    # Restore
    # ========================================================

    @classmethod
    def from_snapshot(
        cls,
        data: Dict[str, Any],
    ) -> "WorkflowState":
        """
        Restore state from snapshot.
        """

        state = cls(
            workflow_id=data["workflow_id"],
            session_id=data.get(
                "session_id"
            ),
        )


        state.current_node = data.get(
            "current_node"
        )

        state.variables = data.get(
            "variables",
            {},
        )

        state.results = data.get(
            "results",
            {},
        )

        state.metadata = data.get(
            "metadata",
            {},
        )


        return state