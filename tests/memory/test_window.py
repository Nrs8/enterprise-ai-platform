"""
Tests for ContextWindow.
"""

from datetime import datetime, timezone


from app.memory.models import Message
from app.memory.window import ContextWindow



def create_message(
    role: str,
    content: str,
) -> Message:
    return Message(
        role=role,
        content=content,
        created_at=datetime.now(timezone.utc),
    )



def test_empty_messages():

    window = ContextWindow(
        max_messages=3
    )

    result = window.build([])

    assert result == []



def test_system_message_is_always_kept():

    window = ContextWindow(
        max_messages=2
    )

    messages = [
        create_message(
            "system",
            "You are helpful",
        ),
        create_message(
            "user",
            "hello",
        ),
        create_message(
            "assistant",
            "hi",
        ),
        create_message(
            "user",
            "question",
        ),
    ]


    result = window.build(
        messages
    )


    assert result[0].role == "system"

    assert len(result) == 3



def test_only_latest_messages_are_kept():

    window = ContextWindow(
        max_messages=2
    )


    messages = [
        create_message(
            "user",
            "message 1",
        ),
        create_message(
            "assistant",
            "message 2",
        ),
        create_message(
            "user",
            "message 3",
        ),
        create_message(
            "assistant",
            "message 4",
        ),
    ]


    result = window.build(
        messages
    )


    assert len(result) == 2

    assert result[0].content == "message 3"

    assert result[1].content == "message 4"