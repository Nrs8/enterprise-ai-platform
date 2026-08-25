from app.memory.context_builder import ContextBuilder
from app.memory.window import ContextWindow

from app.memory.models import Message

from app.runtime.context import AgentContext



def test_context_builder_limits_history():

    window = ContextWindow(
        max_messages=5
    )


    builder = ContextBuilder(
        window
    )


    messages = []


    for i in range(20):

        messages.append(

            Message(

                role="user",

                content=f"message-{i}",

            )

        )


    context = AgentContext(

        session_id="test",

        input="hello",

    )


    builder.apply_history(

        context,

        messages,

    )


    assert len(

        context.history

    ) == 5


    assert (

        context.history[0]

        .content

        ==

        "message-15"

    )





def test_context_builder_keeps_system():

    window = ContextWindow(

        max_messages=3

    )


    builder = ContextBuilder(

        window

    )


    messages = [

        Message(

            role="system",

            content="system",

        ),

        Message(

            role="user",

            content="old",

        ),

        Message(

            role="user",

            content="new",

        ),

    ]


    context = AgentContext(

        session_id="test",

        input="hello",

    )


    builder.apply_history(

        context,

        messages,

    )


    assert len(

        context.history

    ) == 3


    assert (

        context.history[0]

        .role

        ==

        "system"

    )


    assert (

        context.history[0]

        .content

        ==

        "system"

    )