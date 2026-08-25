from app.memory.providers.sqlite_store import (
    SQLiteMemoryStore,
)



def test_sqlite_memory_store():


    store = SQLiteMemoryStore(

        database_path="data/test_memory.db"

    )


    data = {

        "session_id": "test",

        "messages": [

            {

                "role": "user",

                "content": "hello",

            }

        ],

    }



    #
    # Save
    #

    store.save(

        "conversation_test",

        data,

    )



    #
    # Load
    #

    loaded = store.get(

        "conversation_test"

    )



    assert loaded is not None


    assert loaded["session_id"] == "test"


    assert (

        loaded["messages"][0]["content"]

        ==

        "hello"

    )



    #
    # Delete
    #

    store.delete(

        "conversation_test"

    )


    assert store.get(

        "conversation_test"

    ) is None