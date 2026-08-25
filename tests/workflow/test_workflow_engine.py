"""
Workflow engine tests.
"""


import pytest


from app.workflow.models import (
    WorkflowGraph,
    WorkflowNode,
    WorkflowEdge,
)


from app.workflow.engine import (
    WorkflowEngine,
    WorkflowNodeExecutor,
)


from app.workflow.state import (
    WorkflowState,
)





class FakeExecutor(
    WorkflowNodeExecutor
):
    """
    Fake workflow executor.
    """


    def __init__(
        self,
        value: str,
    ):
        self.value = value



    async def execute(
        self,
        state,
    ):

        return {

            "response":

                self.value

        }






@pytest.mark.asyncio
async def test_workflow_engine_execution():

    """
    Workflow:

        node1
          |
          v
        node2
    """


    graph = WorkflowGraph()



    graph.add_node(

        WorkflowNode(

            node_id="node1",

            name="node1",

            node_type="fake",

        )

    )


    graph.add_node(

        WorkflowNode(

            node_id="node2",

            name="node2",

            node_type="fake",

        )

    )



    graph.add_edge(

        WorkflowEdge(

            source="node1",

            target="node2",

        )

    )




    engine = WorkflowEngine()



    engine.register_executor(

        "fake",

        FakeExecutor(

            "hello"

        )

    )




    state = WorkflowState(

        workflow_id="test"

    )



    result = await engine.execute(

        graph,

        state,

    )



    assert result.results[

        "node1"

    ]["response"] == "hello"



    assert result.results[

        "node2"

    ]["response"] == "hello"