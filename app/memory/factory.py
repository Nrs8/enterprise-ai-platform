"""
Memory store factory.

Responsible for creating MemoryStore implementations
based on application configuration.
"""

from __future__ import annotations


from app.memory.interface import MemoryStore
from app.memory.providers.file_store import FileMemoryStore
from app.memory.providers.sqlite_store import SQLiteMemoryStore



def create_memory_store(
    backend: str,
    sqlite_path: str | None = None,
) -> MemoryStore:
    """
    Create memory storage backend.

    Args:
        backend:
            Storage backend name.

        sqlite_path:
            SQLite database path.

    Returns:
        MemoryStore implementation.

    Raises:
        ValueError:
            Unsupported backend.
    """

    if backend == "file":

        return FileMemoryStore()


    if backend == "sqlite":

        if sqlite_path is None:
            raise ValueError(
                "sqlite_path required for sqlite backend"
            )

        return SQLiteMemoryStore(
            sqlite_path
        )


    raise ValueError(
        f"Unsupported memory backend: {backend}"
    )