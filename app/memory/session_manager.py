"""
Session manager for in-memory conversation storage.
"""
from __future__ import annotations
from app.memory.exceptions import SessionNotFoundError
from app.memory.base import SessionManager

from app.memory.models import Message, Session


class InMemorySessionManager(SessionManager):
    """
    Manages conversation sessions in memory.
    """

    def __init__(self) -> None:
        """
        Initialize the in-memory session store.
        """

        self._sessions: dict[str, Session] = {}

    def create_session(self) -> Session:
        """
        Create and store a new session.
        """

        session = Session()
        self._sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Session:
        """
        Retrieve an existing session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """

        session = self._sessions.get(session_id)

        if session is None:
            raise SessionNotFoundError(
                f"Session '{session_id}' does not exist."
            )

        return session



    def add_message(
        self,
        session_id: str,
        message: Message,
    ) -> None:
        """
        Add a message to an existing session.
        """

        session = self.get_session(session_id)
        session.add_message(message)

    def delete_session(self, session_id: str) -> None:
        """
        Delete a session.
        """

        del self._sessions[session_id]