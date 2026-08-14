"""
Agent runtime responsible for conversation orchestration.

Coordinates:

Memory
Governance
Agents
Observability
Audit
"""


import logging


from app.agents.supervisor import SupervisorAgent


from app.memory.models import Message


from app.memory.session_manager import (
    InMemorySessionManager,
)


from app.observability import tracer

from app.observability.metrics import metrics


from app.runtime.context import AgentContext


from app.runtime.steps.governance_step import GovernanceStep



logger = logging.getLogger(
    "app.runtime"
)


logger.setLevel(
    logging.INFO
)



class AgentRuntime:
    """
    Main orchestration runtime.

    Responsibilities:

    - Session lifecycle
    - Governance execution
    - Agent routing
    - Observability
    - Conversation persistence

    Agent reasoning is delegated
    to SupervisorAgent.
    """



    def __init__(

        self,

        session_manager: InMemorySessionManager,

        supervisor_agent: SupervisorAgent,

        governance_step: GovernanceStep,

        tracer=tracer,

    ) -> None:



        #
        # Memory
        #

        self._session_manager = (
            session_manager
        )



        #
        # Agent Router
        #

        self._supervisor_agent = (
            supervisor_agent
        )



        #
        # Governance
        #

        self._governance_step = (
            governance_step
        )



        #
        # Observability
        #

        self.tracer = tracer





    async def chat(

        self,

        session_id: str,

        message: str,

        model: str = "qwen",

        user_id: str = "anonymous",

        tenant_id: str = "default",

    ) -> str:
        """
        Execute one AI conversation turn.
        """



        metrics.increment(
            "requests_total"
        )



        trace = (
            self.tracer.start_trace()
        )



        try:



            context = AgentContext(

                session_id=session_id,

                input=message,

                model=model,

                user_id=user_id,

                tenant_id=tenant_id,

            )



            context.trace = trace




            with self.tracer.span(

                trace,

                "agent_runtime",

                {

                    "session_id":
                        session_id,


                    "user_id":
                        user_id,


                    "tenant_id":
                        tenant_id,


                    "model":
                        model,

                },

            ):



                #
                # Load Session
                #

                context.session = (

                    self._session_manager
                    .get_session(
                        session_id
                    )

                )



                logger.info(

                    "Loaded conversation session",

                    extra={

                        "session_id":
                            session_id,


                        "message_count":
                            len(
                                context.session.messages
                            ),

                    },

                )




                #
                # Governance
                #

                with self.tracer.span(

                    trace,

                    "governance_check",

                ):


                    await self._governance_step.run(

                        context

                    )




                #
                # Agent Execution
                #

                with self.tracer.span(

                    trace,

                    "agent_execution",

                ):


                    result = await (

                        self._supervisor_agent
                        .execute(

                            context

                        )

                    )



                response = (
                    result.response
                )




                #
                # Persist Conversation
                #

                self._session_manager.add_message(

                    session_id,


                    Message(

                        role="user",

                        content=message,

                    )

                )



                self._session_manager.add_message(

                    session_id,


                    Message(

                        role="assistant",

                        content=response,

                    )

                )



                return response



        finally:



            #
            # Always close trace
            #

            trace.finish()



            logger.info(

                "Trace completed",

                extra={

                    "trace_id":
                        trace.trace_id,


                    "duration_ms":
                        trace.duration_ms,


                    "span_count":
                        len(
                            trace.spans
                        ),

                },

            )