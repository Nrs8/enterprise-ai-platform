from contextlib import contextmanager

from app.observability.models import (
    Trace,
    Span,
)


class Tracer:
    """
    Manage traces and spans.
    """

    def __init__(self):
        self._traces: dict[str, Trace] = {}


    def start_trace(self) -> Trace:
        """
        Create a new trace.
        """

        trace = Trace()

        self._traces[
            trace.trace_id
        ] = trace

        return trace


    def get_trace(
        self,
        trace_id: str,
    ) -> Trace | None:

        return self._traces.get(
            trace_id
        )


    @contextmanager
    def span(
        self,
        trace: Trace,
        name: str,
        attributes: dict[str, str] | None = None,
    ):
        """
        Create a span inside trace.
        """

        span = Span(
            name=name,
            attributes=attributes or {},
        )


        trace.spans.append(span)


        try:
            yield span

        finally:
            span.finish()