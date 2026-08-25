"""
Knowledge agent workflow executor.

Adapts KnowledgeAgent
to WorkflowEngine.
"""

from __future__ import annotations


from typing import Any, Dict


from app.workflow.node import (
    WorkflowNodeExecutor,
)

from app.workflow.state import (
    WorkflowState,
)



class KnowledgeAgentExecutor(
    WorkflowNodeExecutor
):
    """
    Executes KnowledgeAgent inside workflow.

    Workflow:

        WorkflowEngine

              |

        KnowledgeAgentExecutor

              |

        AgentContext

              |

        KnowledgeAgent.execute()

    """



    def __init__(
        self,
        agent,
    ) -> None:

        self.agent = agent





    async def execute(
        self,
        state: WorkflowState,
    ) -> Dict[str, Any]:
        """
        Execute knowledge agent.
        """



        context = (
            state.metadata.get(
                "context"
            )
        )


        if context is None:

            raise RuntimeError(
                "AgentContext missing "
                "from WorkflowState"
            )



        result = await self.agent.execute(
            context
        )



        return {

            "knowledge_result": result

        }