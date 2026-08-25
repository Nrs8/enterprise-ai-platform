"""
Tests for memory store factory.
"""

from pathlib import Path

import pytest

from app.memory.factory import create_memory_store
from app.memory.providers.file_store import FileMemoryStore
from app.memory.providers.sqlite_store import SQLiteMemoryStore


def test_create_file_store() -> None:
    """
    Test factory creates FileMemoryStore.
    """

    store = create_memory_store(
        backend="file",
    )

    assert isinstance(
        store,
        FileMemoryStore,
    )


def test_create_sqlite_store(
    tmp_path: Path,
) -> None:
    """
    Test factory creates SQLiteMemoryStore.
    """

    db_path = tmp_path / "memory.db"

    store = create_memory_store(
        backend="sqlite",
        sqlite_path=str(db_path),
    )

    assert isinstance(
        store,
        SQLiteMemoryStore,
    )


def test_create_sqlite_store_without_path() -> None:
    """
    Test sqlite backend requires database path.
    """

    with pytest.raises(
        ValueError,
        match="sqlite_path required",
    ):
        create_memory_store(
            backend="sqlite",
        )


def test_create_unknown_backend() -> None:
    """
    Test unsupported backend raises error.
    """

    with pytest.raises(
        ValueError,
        match="Unsupported memory backend",
    ):
        create_memory_store(
            backend="unknown",
        )