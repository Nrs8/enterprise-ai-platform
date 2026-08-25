"""
Tests for MemoryManager.
"""


from datetime import datetime


from app.memory.manager import (
    MemoryManager,
)


from app.memory.models import (
    UserMemoryEntry,
)


from app.memory.repository import (
    FileConversationRepository,
    FileUserMemoryRepository,
)


from app.memory.providers.file_store import (
    FileMemoryStore,
)

def create_manager(
    tmp_path,
) -> MemoryManager:

    store = FileMemoryStore(
        base_path=str(tmp_path)
    )


    return MemoryManager(

        conversation_repository=
            FileConversationRepository(
                store
            ),


        user_memory_repository=
            FileUserMemoryRepository(
                store
            ),

    )



def test_create_and_get_conversation(
    tmp_path,
):

    manager = create_manager(
        tmp_path
    )


    memory = (
        manager.create_conversation(
            session_id="session-001",
            user_id="user-001",
        )
    )


    assert (
        memory.session_id
        ==
        "session-001"
    )


    loaded = (
        manager.get_conversation(
            "session-001"
        )
    )


    assert loaded is not None


    assert (
        loaded.user_id
        ==
        "user-001"
    )



def test_add_message(
    tmp_path,
):

    manager = create_manager(
        tmp_path
    )


    manager.create_conversation(
        session_id="session-001",
        user_id="user-001",
    )


    manager.add_message(

        session_id="session-001",

        role="user",

        content="hello",

    )


    loaded = (
        manager.get_conversation(
            "session-001"
        )
    )


    assert loaded is not None


    assert len(
        loaded.messages
    ) == 1


    assert (
        loaded.messages[0].content
        ==
        "hello"
    )



def test_create_user_memory(
    tmp_path,
):

    manager = create_manager(
        tmp_path
    )


    memory = (
        manager.create_user_memory(
            "user-001"
        )
    )


    assert (
        memory.user_id
        ==
        "user-001"
    )


    assert (
        memory.memories
        ==
        []
    )



def test_add_user_memory(
    tmp_path,
):

    manager = create_manager(
        tmp_path
    )


    entry = UserMemoryEntry(

        key="language",

        value="Python",

        source="conversation",

        confidence=0.9,

        created_at=datetime.utcnow(),

        updated_at=datetime.utcnow(),

    )


    manager.add_user_memory(

        user_id="user-001",

        entry=entry,

    )


    loaded = (
        manager.get_user_memory(
            "user-001"
        )
    )


    assert loaded is not None


    assert len(
        loaded.memories
    ) == 1


    assert (
        loaded.memories[0].key
        ==
        "language"
    )



def test_find_user_memory(
    tmp_path,
):

    manager = create_manager(
        tmp_path
    )


    manager.add_user_memory(

        user_id="user-001",

        entry=UserMemoryEntry(

            key="name",

            value="Alice",

            source="chat",

            confidence=1.0,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        ),

    )


    result = (
        manager.find_user_memory(
            user_id="user-001",

            key="name",
        )
    )


    assert result is not None


    assert (
        result.value
        ==
        "Alice"
    )