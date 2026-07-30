from app.memory.models import Message


class PromptBuilder:
    """
    Build messages sent to the LLM.
    """

    def __init__(
        self,
        system_prompt: str = "You are a helpful AI assistant.",
    ) -> None:
        """
        Initialize prompt builder.
        """

        self._system_prompt = system_prompt

    def build(
        self,
        history: list[Message],
        user_message: str,
        knowledge_context: str = "",
    ) -> list[Message]:
        """
        Build conversation messages for the LLM.
        """

        system_content = self._system_prompt

        if knowledge_context:
            system_content += (
                "\n\nRelevant Knowledge:\n"
                + knowledge_context
            )

        messages = [
            Message(
                role="system",
                content=system_content,
            )
        ]

        messages.extend(history)

        messages.append(
            Message(
                role="user",
                content=user_message,
            )
        )

        return messages