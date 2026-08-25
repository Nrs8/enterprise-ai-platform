"""
Prompt builder.

Converts runtime agent context
into LLM messages.

Flow:

AgentContext

    |

    v

LLM Messages

    |

    v

LLM Gateway
"""


from __future__ import annotations



from app.llm.models import (
    Message as LLMMessage,
)


from app.runtime.context import (
    AgentContext,
)







class PromptBuilder:
    """
    Build messages sent to LLM.


    Responsibilities:

    - System prompt
    - Memory injection
    - Conversation history
    - Knowledge injection
    - Runtime messages


    Does NOT:

    - Call LLM
    - Execute tools
    - Persist memory
    """





    def __init__(

        self,

        system_prompt: str =
            "You are a helpful AI assistant.",

    ) -> None:
        """
        Initialize prompt builder.
        """


        self._system_prompt = (
            system_prompt
        )









    def build(

        self,

        context: AgentContext,

    ) -> list[LLMMessage]:
        """
        Build final LLM message list.


        Example output:


        [

            SystemMessage,

            UserMessage,

            AssistantMessage,

            UserMessage,

        ]


        """



        messages: list[LLMMessage] = []







        #
        # System Prompt
        #

        system_content = (

            self._system_prompt

        )








        #
        # Inject Memory Context
        #
        # Comes from:
        #
        # MemoryManager
        #      |
        # ContextBuilder
        #      |
        # AgentContext
        #

        if context.memory_context:


            system_content += (

                "\n\nMemory Context:\n"

                +

                self._format_memory_context(

                    context.memory_context

                )

            )









        #
        # Inject Knowledge Context
        #
        # Comes from RAG
        #

        if context.knowledge_context:


            system_content += (

                "\n\nRelevant Knowledge:\n"

                +

                context.knowledge_context

            )










        messages.append(

            LLMMessage(

                role="system",

                content=system_content,

            )

        )









        #
        # Conversation History
        #
        # Persistent memory
        #

        for message in context.history:


            messages.append(

                LLMMessage(

                    role=message.role,

                    content=message.content,

                )

            )









        #
        # Runtime Messages
        #
        # Used by:
        #
        # AgentExecutor
        #
        # Example:
        #
        # assistant tool call
        # tool result
        #

        messages.extend(

            context.messages

        )







        return messages







    def _format_memory_context(

        self,

        memory_context: dict,

    ) -> str:
        """
        Convert memory context
        into readable prompt text.


        Example:

        {
            "user_id":"123",
            "preference":"python"
        }


        becomes:


        user_id: 123

        preference: python

        """


        lines = []


        for key, value in memory_context.items():


            lines.append(

                f"{key}: {value}"

            )


        return "\n".join(

            lines

        )