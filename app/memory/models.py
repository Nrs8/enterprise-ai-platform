"""
Memory domain models.

Defines persistent memory data structures
used by the Agent Runtime.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any



@dataclass
class Message:
    """
    Represents a conversation message.

    Shared by:
    - Memory
    - LLM
    - Agent Runtime
    """

    role: str

    content: str

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )



@dataclass
class ConversationMemory:
    """
    Stores conversation history.

    Represents persistent short-term memory.
    """

    session_id: str

    user_id: str | None = None

    messages: list[Message] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )



@dataclass
class UserMemoryEntry:
    """
    Represents a single long-term user memory item.

    Examples:
    - user preferences
    - user facts
    - learned information
    """

    key: str

    value: Any

    source: str = "unknown"

    confidence: float = 1.0

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )



@dataclass
class UserMemory:
    """
    Stores long-term user information.

    Examples:
    - preferences
    - profile information
    - historical facts
    """

    user_id: str

    memories: list[UserMemoryEntry] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )