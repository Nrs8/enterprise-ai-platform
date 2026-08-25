"""
Observability data models.

Contains:

- Trace
- Span

Used by:

AgentRuntime
AgentExecutor
LLM
Tools
"""

from __future__ import annotations


from dataclasses import dataclass, field

from datetime import datetime, timezone


from typing import Any, Dict, List


import uuid





# ============================================================
# Span
# ============================================================


@dataclass
class Span:
    """
    Single execution span.
    """

    name: str

    start_time: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )

    end_time: datetime | None = None


    attributes: Dict[str, Any] = field(
        default_factory=dict
    )



    def finish(self) -> None:
        """
        Finish span.
        """

        self.end_time = (
            datetime.now(timezone.utc)
        )



    @property
    def duration_ms(self) -> float | None:
        """
        Calculate span duration.
        """

        if self.end_time is None:
            return None


        return (
            self.end_time
            -
            self.start_time
        ).total_seconds() * 1000





# ============================================================
# Trace
# ============================================================


@dataclass
class Trace:
    """
    Represents one agent execution trace.
    """


    trace_id: str = field(
        default_factory=lambda:
            str(uuid.uuid4())
    )


    start_time: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )


    spans: List[Span] = field(
        default_factory=list
    )


    end_time: datetime | None = None


    attributes: Dict[str, Any] = field(
        default_factory=dict
    )



    def finish(self) -> None:
        """
        Finish trace.
        """

        self.end_time = (
            datetime.now(timezone.utc)
        )



    @property
    def duration_ms(self) -> float | None:
        """
        Return trace duration.
        """

        if self.end_time is None:
            return None


        return (
            self.end_time
            -
            self.start_time
        ).total_seconds() * 1000



    def add_span(
        self,
        span: Span,
    ) -> None:
        """
        Add execution span.
        """

        self.spans.append(
            span
        )