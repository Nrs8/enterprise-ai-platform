"""
Tracing infrastructure.

Manage traces, spans and events.
"""


from contextlib import contextmanager

from app.observability.models import (
    Trace,
    Span,
)



class Tracer:
    """
    Manage traces, spans and events.
    """



    def __init__(self):

        self._traces: dict[
            str,
            Trace
        ] = {}


        self._events: list[
            dict
        ] = []


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
        """
        Get trace by id.
        """

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


        trace.spans.append(
            span
        )


        try:

            yield span


        finally:

            span.finish()




    def add_event(
        self,
        name: str,
        attributes: dict | None = None,
    ) -> None:
        """
        Record an observability event.

        Used by agents, governance,
        and routing decisions.
        """

        event = {

            "name": name,

            "attributes": attributes or {},

        }


        self._events.append(
            event
        )




    def get_events(
        self,
    ) -> list[dict]:
        """
        Return recorded events.
        """

        return self._events




# Global Tracer instance

tracer = Tracer()