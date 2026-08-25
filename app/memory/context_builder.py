"""
Runtime context builder.

Builds runtime context from conversation memory.

Responsibilities:

- Apply conversation history windowing
- Inject memory context
- Prepare AgentContext for execution

ContextBuilder does NOT:

- Call LLM
- Execute tools
- Persist memory
"""

from __future__ import annotations

from typing import Any

from app.memory.models import Message
from app.memory.window import ContextWindow
from app.runtime.context import AgentContext


class ContextBuilder:
    """
    Builds runtime context from memory.

    Responsibilities:

        Conversation
             |
             v
        ContextWindow
             |
             v
        AgentContext
    """

    def __init__(
        self,
        context_window: ContextWindow,
    ) -> None:
        """
        Initialize context builder.

        Args:
            context_window:
                Conversation history window policy.
        """

        self._context_window = context_window

    def apply_history(
        self,
        context: AgentContext,
        messages: list[Message],
    ) -> None:
        """
        Apply conversation history to AgentContext.

        The ContextWindow owns history trimming policy.

        ContextBuilder only coordinates:

            raw history
                |
                v
            ContextWindow
                |
                v
            AgentContext.history

        The original message list is not modified.
        """

        trimmed_messages = (
            self._context_window.apply(
                messages
            )
        )

        context.load_history(
            trimmed_messages
        )

    def build(
        self,
        context: AgentContext,
        conversation: Any,
    ) -> None:
        """
        Build runtime context from conversation.

        The conversation object is expected to expose
        its message history through ``messages``.

        Flow:

            Conversation
                 |
                 v
            apply_history()
                 |
                 v
            AgentContext

        Args:
            context:
                Runtime execution context.

            conversation:
                Persistent conversation object.
        """

        messages = list(
            getattr(
                conversation,
                "messages",
                [],
            )
            or []
        )

        self.apply_history(
            context,
            messages,
        )

        self._build_memory_context(
            context
        )

    def _build_memory_context(
        self,
        context: AgentContext,
    ) -> None:
        """
        Build injected long-term memory context.

        Long-term memory injection is intentionally
        kept separate from conversation history.

        Currently this method preserves the existing
        memory context already present in AgentContext.
        """

        if context.memory_context is None:
            context.set_memory_context(
                {}
            )

    def set_memory_context(
        self,
        context: AgentContext,
        memory_context: dict[str, Any],
    ) -> None:
        """
        Inject long-term memory context.

        This method provides an explicit API for
        future memory retrieval components.
        """

        context.set_memory_context(
            memory_context
        )