"""
Memory abstraction interfaces.
"""

from abc import ABC, abstractmethod

from app.memory.models import Message, Session


class SessionManager(ABC):
    """
    Defines conversation session management behavior.
    """

    @abstractmethod
    def create_session(self) -> Session:
        """
        Create a new conversation session.
        """
        pass

    @abstractmethod
    def get_session(
        self,
        session_id: str,
    ) -> Session:
        """
        Retrieve an existing session.
        """
        pass

    @abstractmethod
    def add_message(
        self,
        session_id: str,
        message: Message,
    ) -> None:
        """
        Add a message to a session.
        """
        pass

    @abstractmethod
    def delete_session(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a conversation session.
        """
        pass