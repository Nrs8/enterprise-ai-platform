"""
AI audit logging service.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.audit.models import AuditRecord


class AuditLogger:
    """
    Stores and queries AI governance audit records.

    The current implementation uses in-memory storage.
    Persistence can be introduced behind this service later
    without changing governance callers.
    """

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def record(
        self,
        user_id: str,
        tenant_id: str,
        model: str,
        action: str,
        result: str,
        reason: str,
        metadata: dict[str, Any] | None = None,
    ) -> AuditRecord:
        """
        Create and store an audit record.
        """

        record = AuditRecord(
            user_id=user_id,
            tenant_id=tenant_id,
            model=model,
            action=action,
            result=result,
            reason=reason,
            timestamp=datetime.now(timezone.utc),
            metadata=dict(metadata or {}),
        )

        self._records.append(record)

        return record

    def get_all(self) -> list[AuditRecord]:
        """
        Return a copy of all audit records.
        """

        return self._records.copy()

    def query(
        self,
        user_id: str | None = None,
        tenant_id: str | None = None,
        model: str | None = None,
        action: str | None = None,
        result: str | None = None,
    ) -> list[AuditRecord]:
        """
        Query audit records using optional filters.

        All supplied filters must match.
        """

        records = self._records

        if user_id is not None:
            records = [
                record
                for record in records
                if record.user_id == user_id
            ]

        if tenant_id is not None:
            records = [
                record
                for record in records
                if record.tenant_id == tenant_id
            ]

        if model is not None:
            records = [
                record
                for record in records
                if record.model == model
            ]

        if action is not None:
            records = [
                record
                for record in records
                if record.action == action
            ]

        if result is not None:
            records = [
                record
                for record in records
                if record.result == result
            ]

        return records.copy()

    def count(self) -> int:
        """
        Return the number of stored audit records.
        """

        return len(self._records)

    def clear(self) -> None:
        """
        Remove all stored audit records.
        """

        self._records.clear()