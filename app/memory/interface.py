"""
Memory repository interfaces.

Defines abstraction contracts for
persistent memory implementations.
"""

from abc import ABC, abstractmethod

from app.memory.models import (
    ConversationMemory,
    UserMemory,
)


class ConversationRepository(ABC):
    """
    Defines conversation memory operations.
    """

    @abstractmethod
    def save(
        self,
        memory: ConversationMemory,
    ) -> None:
        """
        Persist conversation memory.
        """
        pass


    @abstractmethod
    def get(
        self,
        session_id: str,
    ) -> ConversationMemory | None:
        """
        Retrieve conversation memory.
        """
        pass


    @abstractmethod
    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Delete conversation memory.
        """
        pass



class UserMemoryRepository(ABC):
    """
    Defines user memory operations.
    """

    @abstractmethod
    def save(
        self,
        memory: UserMemory,
    ) -> None:
        """
        Persist user memory.
        """
        pass


    @abstractmethod
    def get(
        self,
        user_id: str,
    ) -> UserMemory | None:
        """
        Retrieve user memory.
        """
        pass


    @abstractmethod
    def update(
        self,
        memory: UserMemory,
    ) -> None:
        """
        Update user memory.
        """
        pass


    @abstractmethod
    def delete(
        self,
        user_id: str,
    ) -> None:
        """
        Delete user memory.
        """
        pass



class MemoryStore(ABC):
    """
    Base abstraction for memory storage backend.

    Implementations may use:
    - File system
    - Redis
    - PostgreSQL
    """

    @abstractmethod
    def save(
        self,
        key: str,
        value: dict,
    ) -> None:
        """
        Store value by key.
        """
        pass


    @abstractmethod
    def get(
        self,
        key: str,
    ) -> dict | None:
        """
        Retrieve value by key.
        """
        pass


    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        """
        Remove value.
        """
        pass