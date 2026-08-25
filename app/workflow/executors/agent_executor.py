"""
Agent workflow executor.

Bridges:

WorkflowNode

    |

AgentRegistry

    |

Agent

    |

AgentResult
"""


from __future__ import annotations


import logging


from typing import Any, Dict



from app.workflow.engine import (
    WorkflowNodeExecutor,
)


from app.workflow.models import (
    WorkflowState,
)



from app.agents.registry import (
    AgentRegistry,
)



from app.runtime.context import (
    AgentContext,
)





logger = logging.getLogger(
    "app.workflow.agent_executor"
)







class AgentWorkflowExecutor(
    WorkflowNodeExecutor
):
    """
    Executes workflow nodes
    through Agent system.


    Flow:


    WorkflowState

          |

          v

    AgentContext

          |

          v

    AgentRegistry

          |

          v

    Agent.execute()

          |

          v

    AgentResult

    """





    def __init__(

        self,

        agent_registry: AgentRegistry,

    ) -> None:


        self._agent_registry = (
            agent_registry
        )









    async def execute(

        self,

        state: WorkflowState,

    ) -> Dict[str, Any]:
        """
        Execute one workflow node.
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







        node = (

            self._find_current_node(

                state

            )

        )



        if node is None:


            raise RuntimeError(

                "Current workflow node not found"

            )







        agent_name = (

            self._resolve_agent(

                node.node_type

            )

        )







        agent = (

            self._agent_registry.get(

                agent_name

            )

        )







        if agent is None:


            raise RuntimeError(

                f"Agent not found: {agent_name}"

            )







        logger.info(

            "Executing agent=%s",

            agent_name,

        )







        result = await (

            agent.execute(

                context

            )

        )







        return {

            "response":

                result.response,


            "success":

                result.success,


            "agent":

                result.agent,


            "error":

                result.error,

        }











    def _resolve_agent(

        self,

        node_type: str,

    ) -> str:
        """
        Resolve workflow node type
        into agent name.


        Example:


        tool

          |

          v

        tool_agent


        knowledge

          |

          v

        knowledge_agent

        """



        mapping = {


            "tool":

                "tool_agent",



            "knowledge":

                "knowledge_agent",

        }



        return mapping.get(

            node_type,

            node_type,

        )









    def _find_current_node(

        self,

        state: WorkflowState,

    ):

        """
        Placeholder.

        Current node lookup will later
        move into WorkflowExecutionContext.
        """

        graph = state.metadata.get(

            "graph"

        )


        if graph is None:

            return None



        return graph.nodes.get(

            state.current_node

        )