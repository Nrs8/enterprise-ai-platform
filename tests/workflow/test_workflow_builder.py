"""
Workflow builder tests.
"""


from app.planning.models import (
    ExecutionPlan,
    PlanStep,
    TaskType,
)


from app.planning.workflow_builder import (
    WorkflowBuilder,
)





def test_workflow_builder_creates_graph():
    """
    ExecutionPlan should become WorkflowGraph.
    """



    plan = ExecutionPlan(

        steps=[

            PlanStep(

                name="step1",

                task_type=TaskType.TOOL,

                description="calculate 1+1",

            ),



            PlanStep(

                name="step2",

                task_type=TaskType.KNOWLEDGE,

                description="search document",

            ),

        ]

    )





    builder = WorkflowBuilder()



    graph = builder.build(

        plan

    )





    #
    # Nodes
    #

    assert "step1" in graph.nodes

    assert "step2" in graph.nodes





    assert (

        graph.nodes["step1"]

        .node_type

        == "tool"

    )



    assert (

        graph.nodes["step2"]

        .node_type

        == "knowledge"

    )





    #
    # Metadata
    #

    assert (

        graph.nodes["step1"]

        .metadata["task"]

        == "calculate 1+1"

    )





    #
    # Edge
    #

    assert len(

        graph.edges

    ) == 1




    assert (

        graph.edges[0].source

        == "step1"

    )


    assert (

        graph.edges[0].target

        == "step2"

    )