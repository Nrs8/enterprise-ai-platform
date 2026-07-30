from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from app.llm.models import ToolCall

def utc_now() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.
    """

    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Message:
    """
    Represents a single chat message.
    """

    role: str
    content: str
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Session:
    """
    Represents a conversation session.
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=utc_now)

    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation history.
        """

        self.messages.append(message)