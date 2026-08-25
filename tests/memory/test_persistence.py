from app.memory.providers.file_store import (
    FileMemoryStore,
)

from app.memory.repository import (
    FileConversationRepository,
)

from app.memory.models import (
    ConversationMemory,
    Message,
)





def test_conversation_persistence():


    #
    # Storage
    #

    store = FileMemoryStore()



    repository = FileConversationRepository(

        store

    )



    #
    # Create conversation
    #

    memory = ConversationMemory(

        session_id="test-session",

        user_id="user-1",

    )



    memory.messages.append(

        Message(

            role="user",

            content="hello",

        )

    )



    #
    # Save
    #

    repository.save(

        memory

    )



    #
    # Reload
    #

    loaded = repository.get(

        "test-session"

    )



    #
    # Verify
    #

    assert loaded is not None


    assert loaded.session_id == (

        "test-session"

    )


    assert len(

        loaded.messages

    ) == 1


    assert (

        loaded.messages[0].content

        ==

        "hello"

    )