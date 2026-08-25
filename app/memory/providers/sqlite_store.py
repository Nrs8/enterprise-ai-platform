"""
SQLite based memory storage provider.

Provides persistent storage using SQLite.
"""

from __future__ import annotations


import json
import sqlite3

from pathlib import Path
from typing import Any


from app.memory.interface import MemoryStore





class SQLiteMemoryStore(MemoryStore):
    """
    SQLite based memory store.

    Implements MemoryStore interface.
    """



    def __init__(
        self,
        database_path: str = "data/memory.db",
    ) -> None:


        self.database_path = Path(
            database_path
        )


        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        self._initialize()






    def _initialize(self) -> None:
        """
        Create database schema.
        """


        with sqlite3.connect(
            self.database_path
        ) as connection:


            connection.execute(

                """
                CREATE TABLE IF NOT EXISTS memory_store (

                    key TEXT PRIMARY KEY,

                    value TEXT NOT NULL

                )
                """

            )


            connection.commit()







    def save(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        """
        Persist dictionary data.
        """


        serialized = json.dumps(

            value,

            ensure_ascii=False,

        )


        with sqlite3.connect(

            self.database_path

        ) as connection:


            connection.execute(

                """
                INSERT INTO memory_store
                (
                    key,
                    value
                )

                VALUES (?, ?)

                ON CONFLICT(key)

                DO UPDATE SET

                    value = excluded.value

                """,

                (
                    key,
                    serialized,
                ),

            )


            connection.commit()







    def get(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        """
        Load dictionary data.
        """


        with sqlite3.connect(

            self.database_path

        ) as connection:


            cursor = connection.execute(

                """
                SELECT value

                FROM memory_store

                WHERE key = ?

                """,

                (
                    key,
                ),

            )


            row = cursor.fetchone()



            if row is None:

                return None



            return json.loads(

                row[0]

            )








    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete stored data.
        """


        with sqlite3.connect(

            self.database_path

        ) as connection:


            connection.execute(

                """
                DELETE FROM memory_store

                WHERE key = ?

                """,

                (
                    key,
                ),

            )


            connection.commit()