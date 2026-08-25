"""
Memory manager.

Provides unified access to:

- Conversation memory
- User memory
"""


from datetime import datetime, timezone


from app.memory.models import (
    ConversationMemory,
    UserMemory,
    UserMemoryEntry,
    Message,
)


from app.memory.interface import (
    ConversationRepository,
    UserMemoryRepository,
)



class MemoryManager:
    """
    High level memory service.

    Abstracts memory persistence
    from runtime layer.
    """


    def __init__(

        self,

        conversation_repository:
            ConversationRepository,


        user_memory_repository:
            UserMemoryRepository,

    ) -> None:


        self._conversation_repository = (
            conversation_repository
        )


        self._user_memory_repository = (
            user_memory_repository
        )



    #
    # ============================
    # Conversation Memory
    # ============================
    #


    def create_conversation(

        self,

        session_id: str,

        user_id: str,

    ) -> ConversationMemory:
        """
        Create new conversation memory.
        """


        now = datetime.now(timezone.utc)


        memory = ConversationMemory(

            session_id=session_id,

            user_id=user_id,

            messages=[],

            created_at=now,

            updated_at=now,

        )


        self._conversation_repository.save(
            memory
        )


        return memory



    def get_conversation(

        self,

        session_id: str,

    ) -> ConversationMemory | None:
        """
        Load conversation memory.
        """


        return (
            self._conversation_repository
            .get(
                session_id
            )
        )



    def add_message(

        self,

        session_id: str,

        role: str,

        content: str,

    ) -> None:
        """
        Append message into conversation.
        """


        conversation = (
            self.get_conversation(
                session_id
            )
        )


        if conversation is None:

            raise ValueError(
                f"Conversation not found: {session_id}"
            )



        conversation.messages.append(

            Message(

                role=role,

                content=content,

            )

        )


        conversation.updated_at = (
            datetime.utcnow()
        )


        self._conversation_repository.save(
            conversation
        )



    #
    # ============================
    # User Memory
    # ============================
    #



    def get_user_memory(

        self,

        user_id: str,

    ) -> UserMemory | None:
        """
        Load user memory.
        """


        return (
            self._user_memory_repository
            .get(
                user_id
            )
        )



    def create_user_memory(

        self,

        user_id: str,

    ) -> UserMemory:
        """
        Create empty user memory.
        """


        memory = UserMemory(

            user_id=user_id,

            memories=[],

        )


        self._user_memory_repository.save(
            memory
        )


        return memory



    def add_user_memory(

        self,

        user_id: str,

        entry: UserMemoryEntry,

    ) -> UserMemory:
        """
        Add one UserMemoryEntry.
        """


        memory = (
            self.get_user_memory(
                user_id
            )
        )


        if memory is None:

            memory = (
                self.create_user_memory(
                    user_id
                )
            )


        memory.memories.append(
            entry
        )


        self._user_memory_repository.save(
            memory
        )


        return memory



    def find_user_memory(

        self,

        user_id: str,

        key: str,

    ) -> UserMemoryEntry | None:
        """
        Find memory entry by key.
        """


        memory = (
            self.get_user_memory(
                user_id
            )
        )


        if memory is None:

            return None



        for entry in memory.memories:

            if entry.key == key:

                return entry



        return None