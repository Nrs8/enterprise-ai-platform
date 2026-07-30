from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Span:
    """
    Represents one operation inside a trace.
    """

    name: str

    span_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    start_time: datetime = field(
        default_factory=datetime.utcnow
    )

    end_time: datetime | None = None

    attributes: dict[str, str] = field(
        default_factory=dict
    )

    def finish(self) -> None:
        self.end_time = datetime.utcnow()

    @property
    def duration_ms(self) -> float | None:
        """
        Return span duration in milliseconds.
        """

        if self.end_time is None:
            return None

        return (
            self.end_time - self.start_time
        ).total_seconds() * 1000


@dataclass
class Trace:
    """
    Represents one complete request execution.
    """

    trace_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    start_time: datetime = field(
        default_factory=datetime.utcnow
    )

    end_time: datetime | None = None

    spans: list[Span] = field(
        default_factory=list
    )

    def finish(self) -> None:
        self.end_time = datetime.utcnow()

    @property
    def duration_ms(self) -> float | None:
        """
        Return trace duration in milliseconds.
        """

        if self.end_time is None:
            return None

        return (
            self.end_time - self.start_time
        ).total_seconds() * 1000