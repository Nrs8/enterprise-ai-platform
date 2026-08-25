from app.memory.context_builder import ContextBuilder
from app.memory.window import ContextWindow

from app.memory.models import Message

from app.runtime.context import AgentContext




def test_long_history_is_trimmed_before_runtime():


    #
    # Context policy
    #

    window = ContextWindow(

        max_messages=20

    )


    builder = ContextBuilder(

        context_window=window

    )



    #
    # Simulate long conversation
    #

    messages = []


    for i in range(500):

        messages.append(

            Message(

                role="user",

                content=f"user-message-{i}",

            )

        )



    #
    # Runtime context
    #

    context = AgentContext(

        session_id="long-session",

        input="latest question",

    )



    #
    # Apply memory window
    #

    builder.apply_history(

        context,

        messages,

    )



    #
    # Verify pollution prevention
    #

    assert len(

        context.history

    ) == 20



    assert (

        context.history[0]

        .content

        ==

        "user-message-480"

    )



    assert (

        context.history[-1]

        .content

        ==

        "user-message-499"

    )