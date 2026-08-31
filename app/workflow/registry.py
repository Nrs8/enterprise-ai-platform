"""
Workflow registry.

Manages available business workflows.
"""

from __future__ import annotations


from typing import Dict, Any





class WorkflowRegistry:
    """
    Registry for workflow definitions.
    """



    def __init__(
        self,
    ) -> None:

        self._workflows: Dict[
            str,
            Any,
        ] = {}





    def register(
        self,
        workflow,
    ) -> None:
        """
        Register workflow.
        """

        self._workflows[
            workflow.name
        ] = workflow





    def get(
        self,
        name: str,
    ):
        """
        Retrieve workflow.
        """

        if name not in self._workflows:

            raise ValueError(
                f"Workflow not found: {name}"
            )


        return self._workflows[name]





    def list_workflows(
        self,
    ) -> list[str]:
        """
        List registered workflows.
        """

        return list(
            self._workflows.keys()
        )