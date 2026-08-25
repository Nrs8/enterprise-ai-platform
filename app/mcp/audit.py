"""
MCP audit layer.

Provides structured audit events
for MCP tool invocations.
"""

from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class MCPAuditEvent:
    """
    Represents a single MCP tool execution audit event.
    """

    tenant_id: str

    server_name: str

    tool_name: str

    success: bool

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    error: Optional[str] = None


class MCPAuditLogger:
    """
    Collects MCP audit events.

    Current implementation:
    in-memory storage.

    Future implementations may persist
    events into database or event streams.
    """

    def __init__(self) -> None:
        self._events: List[MCPAuditEvent] = []


    def record(
        self,
        event: MCPAuditEvent,
    ) -> None:
        """
        Store an audit event.
        """

        self._events.append(event)


    def list_events(
        self,
    ) -> List[MCPAuditEvent]:
        """
        Return all audit events.
        """

        return list(self._events)


    def clear(
        self,
    ) -> None:
        """
        Remove all stored audit events.
        """

        self._events.clear()