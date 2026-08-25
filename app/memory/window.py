"""
Context window management.

Responsible for selecting messages
that should be sent to LLM.
"""

from __future__ import annotations


from app.memory.models import Message



class ContextWindow:
    """
    Selects relevant messages from full history.

    Memory keeps everything.
    ContextWindow decides what LLM sees.
    """


    def __init__(
        self,
        max_messages: int = 20,
    ) -> None:

        self.max_messages = max_messages



    def apply(
        self,
        messages: list[Message],
    ) -> list[Message]:
        """
        Apply context window policy.

        Rules:

        1. Keep system messages.
        2. Keep latest conversation messages.
        """

        if not messages:
            return []


        system_messages = [
            message
            for message in messages
            if message.role == "system"
        ]


        conversation_messages = [
            message
            for message in messages
            if message.role != "system"
        ]


        recent_messages = (
            conversation_messages[
                -self.max_messages:
            ]
        )


        return (
            system_messages
            +
            recent_messages
        )



    #
    # Backward compatibility
    #
    def build(
        self,
        messages: list[Message],
    ) -> list[Message]:
        """
        Deprecated alias.

        Kept for old callers.
        """

        return self.apply(
            messages
        )