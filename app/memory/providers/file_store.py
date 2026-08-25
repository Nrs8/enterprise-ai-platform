"""
File based memory storage provider.

Provides persistent storage using JSON files.
"""


import json


from pathlib import Path
from typing import Any


from app.memory.interface import MemoryStore



class FileMemoryStore(
    MemoryStore
):
    """
    JSON file based memory store.

    Implements MemoryStore interface.
    """


    def __init__(
        self,
        base_path: str = "data/memory",
    ) -> None:


        self.base_path = Path(
            base_path
        )


        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )



    def _get_file_path(
        self,
        key: str,
    ) -> Path:
        """
        Convert key into file path.
        """


        safe_key = (
            key
            .replace(
                "/",
                "_",
            )
            .replace(
                ":",
                "_",
            )
        )


        return (
            self.base_path
            /
            f"{safe_key}.json"
        )



    def save(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        """
        Persist dictionary data.
        """


        file_path = (
            self._get_file_path(
                key
            )
        )


        with file_path.open(
            "w",
            encoding="utf-8",
        ) as file:


            json.dump(

                value,

                file,

                ensure_ascii=False,

                indent=2,

                default=str,

            )



    def get(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        """
        Load dictionary data.
        """


        file_path = (
            self._get_file_path(
                key
            )
        )


        if not file_path.exists():

            return None



        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:


            return json.load(
                file
            )



    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete stored data.
        """


        file_path = (
            self._get_file_path(
                key
            )
        )


        if file_path.exists():

            file_path.unlink()