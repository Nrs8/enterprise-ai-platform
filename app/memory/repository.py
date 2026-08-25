"""
Memory repository implementations.

Provides repository implementations
using storage providers.
"""


from datetime import datetime


from app.memory.interface import (
    ConversationRepository,
    UserMemoryRepository,
    MemoryStore,
)


from app.memory.models import (
    ConversationMemory,
    Message,
    UserMemory,
    UserMemoryEntry,
)



class FileConversationRepository(
    ConversationRepository
):
    """
    Conversation repository using MemoryStore.
    """


    def __init__(
        self,
        store: MemoryStore,
    ) -> None:

        self.store = store



    def save(
        self,
        memory: ConversationMemory,
    ) -> None:
        """
        Persist conversation memory.
        """


        data = {

            "session_id":
                memory.session_id,

            "user_id":
                memory.user_id,


            "messages": [

                {

                    "role":
                        message.role,

                    "content":
                        message.content,

                    "created_at":
                        message.created_at.isoformat(),

                }

                for message in memory.messages

            ],


            "created_at":
                memory.created_at.isoformat(),


            "updated_at":
                memory.updated_at.isoformat(),

        }


        self.store.save(

            f"conversation:{memory.session_id}",

            data,

        )



    def get(
        self,
        session_id: str,
    ) -> ConversationMemory | None:
        """
        Retrieve conversation memory.
        """


        data = self.store.get(

            f"conversation:{session_id}"

        )


        if data is None:

            return None



        messages = [

            Message(

                role=item["role"],

                content=item["content"],

                created_at=datetime.fromisoformat(
                    item["created_at"]
                ),

            )

            for item in data.get(
                "messages",
                [],
            )

        ]



        return ConversationMemory(

            session_id=data["session_id"],

            user_id=data.get(
                "user_id"
            ),

            messages=messages,


            created_at=datetime.fromisoformat(

                data["created_at"]

            ),


            updated_at=datetime.fromisoformat(

                data["updated_at"]

            ),

        )



    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Delete conversation memory.
        """


        self.store.delete(

            f"conversation:{session_id}"

        )





class FileUserMemoryRepository(
    UserMemoryRepository
):
    """
    User memory repository using MemoryStore.
    """


    def __init__(
        self,
        store: MemoryStore,
    ) -> None:

        self.store = store



    def save(
        self,
        memory: UserMemory,
    ) -> None:
        """
        Persist user memory.
        """


        data = {

            "user_id":
                memory.user_id,


            "memories": [

                {

                    "key":
                        entry.key,

                    "value":
                        entry.value,

                    "source":
                        entry.source,

                    "confidence":
                        entry.confidence,


                    "created_at":
                        entry.created_at.isoformat(),


                    "updated_at":
                        entry.updated_at.isoformat(),

                }

                for entry in memory.memories

            ],

        }


        self.store.save(

            f"user_memory:{memory.user_id}",

            data,

        )



    def get(
        self,
        user_id: str,
    ) -> UserMemory | None:
        """
        Retrieve user memory.
        """


        data = self.store.get(

            f"user_memory:{user_id}"

        )


        if data is None:

            return None



        memories = [

            UserMemoryEntry(

                key=item["key"],

                value=item["value"],

                source=item.get(
                    "source",
                    "unknown",
                ),

                confidence=item.get(
                    "confidence",
                    0.0,
                ),

                created_at=datetime.fromisoformat(

                    item["created_at"]

                ),


                updated_at=datetime.fromisoformat(

                    item["updated_at"]

                ),

            )

            for item in data.get(
                "memories",
                [],
            )

        ]



        return UserMemory(

            user_id=user_id,

            memories=memories,

        )



    def update(
        self,
        memory: UserMemory,
    ) -> None:
        """
        Update user memory.
        """


        self.save(
            memory
        )



    def delete(
        self,
        user_id: str,
    ) -> None:
        """
        Delete user memory.
        """


        self.store.delete(

            f"user_memory:{user_id}"

        )