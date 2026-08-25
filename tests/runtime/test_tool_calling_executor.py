"""
Tests for ToolCallingExecutor.
"""


from unittest.mock import AsyncMock, Mock

import pytest

from app.runtime.executor.tool_calling_executor import (
    ToolCallingExecutor,
)



class FakeResponse:
    """
    Fake LLM response.
    """

    def __init__(
        self,
        content="",
        tool_calls=None,
    ):

        self.content = content
        self.tool_calls = tool_calls





class FakeToolCall:
    """
    Fake tool call.
    """

    def __init__(self):

        self.name = "calculator"
        self.id = "call-1"
        self.arguments = {
            "expression": "8*6"
        }





class FakeToolResult:
    """
    Fake tool result.
    """

    def __init__(
        self,
        success=True,
        content="48",
    ):

        self.success = success
        self.content = content
        self.error = None





class FakeContext:
    """
    Minimal runtime context.
    """

    def __init__(self):

        self.trace = Mock()

        self.response = None

        self.llm_response = None

        self.assistant_messages = []

        self.tool_messages = []



    def set_response(
        self,
        response,
    ):

        self.response = response



    def add_assistant_message(
        self,
        content,
        tool_calls,
    ):

        self.assistant_messages.append(
            {
                "content": content,
                "tool_calls": tool_calls,
            }
        )



    def add_tool_message(
        self,
        content,
        tool_call_id,
    ):

        self.tool_messages.append(
            {
                "content": content,
                "tool_call_id": tool_call_id,
            }
        )





@pytest.fixture
def tracer():

    mock = Mock()

    mock.span.return_value.__enter__ = Mock()

    mock.span.return_value.__exit__ = Mock(
        return_value=None
    )

    return mock





@pytest.mark.asyncio
async def test_tool_calling_executor_final_answer(
    tracer,
):

    llm_step = AsyncMock()

    llm_step.execute.return_value = FakeResponse(
        content="final answer",
        tool_calls=None,
    )


    tool_step = AsyncMock()


    executor = ToolCallingExecutor(
        llm_step=llm_step,
        tool_step=tool_step,
        tracer=tracer,
    )


    context = FakeContext()


    result = await executor.execute(
        context
    )


    assert result == "final answer"

    assert context.response == "final answer"





@pytest.mark.asyncio
async def test_tool_calling_executor_executes_tool(
    tracer,
):

    llm_step = AsyncMock()


    llm_step.execute.side_effect = [

        FakeResponse(
            content="",
            tool_calls=[
                FakeToolCall()
            ],
        ),

        FakeResponse(
            content="answer after tool",
            tool_calls=None,
        ),
    ]


    tool_step = AsyncMock()

    tool_step.execute_tool.return_value = (
        FakeToolResult()
    )


    executor = ToolCallingExecutor(
        llm_step=llm_step,
        tool_step=tool_step,
        tracer=tracer,
    )


    context = FakeContext()


    result = await executor.execute(
        context
    )


    assert result == "answer after tool"


    tool_step.execute_tool.assert_called_once_with(
        tool_name="calculator",
        arguments={
            "expression": "8*6"
        },
    )


    assert len(
        context.tool_messages
    ) == 1





@pytest.mark.asyncio
async def test_tool_failure_creates_error_message(
    tracer,
):

    llm_step = AsyncMock()


    llm_step.execute.side_effect = [

        FakeResponse(
            tool_calls=[
                FakeToolCall()
            ],
        ),

        FakeResponse(
            content="handled",
            tool_calls=None,
        ),
    ]


    tool_step = AsyncMock()

    result = FakeToolResult(
        success=False,
        content=None,
    )

    result.error = "failed"

    tool_step.execute_tool.return_value = result


    executor = ToolCallingExecutor(
        llm_step=llm_step,
        tool_step=tool_step,
        tracer=tracer,
    )


    context = FakeContext()


    await executor.execute(
        context
    )


    assert (
        "Tool execution failed"
        in
        context.tool_messages[0]["content"]
    )





@pytest.mark.asyncio
async def test_tool_calling_executor_max_iterations(
    tracer,
):

    llm_step = AsyncMock()

    llm_step.execute.return_value = FakeResponse(
        tool_calls=[
            FakeToolCall()
        ],
    )


    tool_step = AsyncMock()

    tool_step.execute_tool.return_value = (
        FakeToolResult()
    )


    executor = ToolCallingExecutor(
        llm_step=llm_step,
        tool_step=tool_step,
        tracer=tracer,
        max_iterations=2,
    )


    context = FakeContext()


    with pytest.raises(RuntimeError):

        await executor.execute(
            context
        )