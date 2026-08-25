"""
Agent runtime responsible for conversation orchestration.

Coordinates:

- Memory
- Governance
- Planning
- Workflow Execution
- Observability
- Conversation Persistence


Runtime does NOT perform reasoning.

Reasoning belongs to Agents.
"""


from __future__ import annotations


import logging

from contextlib import nullcontext


from app.agents.models import AgentResult

from app.memory.manager import MemoryManager
from app.memory.context_builder import ContextBuilder

from app.agents.supervisor import SupervisorAgent
from app.agents.executor import AgentExecutor
from app.agents.registry import AgentRegistry

from app.planning.planner import Planner
from app.planning.executor import PlanExecutor

from app.workflow.state import WorkflowState

from app.observability import tracer

from app.observability.metrics import metrics

from app.runtime.context import AgentContext

from app.runtime.steps.governance_step import GovernanceStep

from app.runtime.errors import build_error_info



logger = logging.getLogger(
    "app.runtime"
)


logger.setLevel(
    logging.INFO
)





def _safe_span(
    tracer_instance,
    trace,
    name: str,
):
    """
    Support real tracer and mocked tracer.

    Unit tests may inject Mock tracer.
    """

    try:

        span = tracer_instance.span(
            trace,
            name,
        )


        if hasattr(
            span,
            "__enter__",
        ):
            return span


    except Exception:
        pass


    return nullcontext()







class AgentRuntime:
    """
    Main agent orchestration runtime.


    Responsibilities:

    - Conversation lifecycle
    - Memory loading
    - Context construction
    - Governance validation
    - Supervisor routing
    - Planning
    - Workflow execution
    - Agent execution
    - Persistence
    - Observability


    Runtime does NOT:

    - call LLM directly
    - execute tools
    - perform reasoning
    """



    def __init__(

        self,

        memory_manager: MemoryManager,

        context_builder: ContextBuilder,

        supervisor_agent: SupervisorAgent,

        agent_registry: AgentRegistry,

        agent_executor: AgentExecutor,

        governance_step: GovernanceStep,

        planner: Planner | None = None,

        plan_executor: PlanExecutor | None = None,

        tracer=tracer,

    ) -> None:


        self._memory_manager = (
            memory_manager
        )


        self._context_builder = (
            context_builder
        )


        self._supervisor_agent = (
            supervisor_agent
        )


        self._agent_registry = (
            agent_registry
        )


        self._agent_executor = (
            agent_executor
        )


        self._governance_step = (
            governance_step
        )


        self._planner = planner


        self._plan_executor = (
            plan_executor
        )


        self.tracer = tracer







    async def chat(

        self,

        session_id: str,

        message: str,

        model: str = "qwen",

        user_id: str = "anonymous",

        tenant_id: str = "default",

    ) -> AgentResult:

        """
        Execute one conversation turn.
        """


        metrics.increment(
            "requests_total"
        )



        trace = (
            self.tracer.start_trace()
        )



        try:


            with _safe_span(

                self.tracer,

                trace,

                "agent_runtime",

            ):



                #
                # 1.
                # Load conversation
                #

                conversation = (
                    self._memory_manager
                    .get_conversation(
                        session_id
                    )
                )



                if conversation is None:


                    conversation = (
                        self._memory_manager
                        .create_conversation(
                            session_id=session_id,
                            user_id=user_id,
                        )
                    )



                #
                # 2.
                # Persist user message
                #

                self._memory_manager.add_message(

                    session_id=session_id,

                    role="user",

                    content=message,

                )



                #
                # 3.
                # Reload memory
                #

                conversation = (
                    self._memory_manager
                    .get_conversation(
                        session_id
                    )
                )



                if conversation is None:

                    raise RuntimeError(
                        "Conversation missing"
                    )




                #
                # 4.
                # Build context
                #

                context = AgentContext(

                    session_id=session_id,

                    input=message,

                    model=model,

                    user_id=user_id,

                    tenant_id=tenant_id,

                    trace=trace,

                )


                context.session = conversation




                #
                # 5.
                # Context window
                #

                self._context_builder.build(

                    context,

                    conversation,

                )




                #
                # 6.
                # Governance
                #

                await self._governance_step.run(

                    context

                )





                #
                # 7.
                # Supervisor routing
                #

                decision = await (

                    self._supervisor_agent

                    .decide(

                        context

                    )

                )



                context.metadata[

                    "agent_decision"

                ] = decision





                #
                # 8.
                # Execute agent
                #

                result: AgentResult



                agent = (

                    self._agent_registry

                    .get(

                        decision.agent_name

                    )

                )



                if agent is None:


                    raise RuntimeError(

                        f"Agent not found: "

                        f"{decision.agent_name}"

                    )




                result = await (

                    self._agent_executor

                    .execute(

                        agent,

                        context,

                    )

                )




                if not result.success:

                    return result





                #
                # 9.
                # Update context
                #

                context.set_response(

                    result.response or ""

                )





                #
                # 10.
                # Save assistant message
                #

                self._memory_manager.add_message(

                    session_id=session_id,

                    role="assistant",

                    content=result.response or "",

                )





                #
                # 11.
                # Return
                #

                return AgentResult.success_result(

                    response=result.response or "",

                    agent=result.agent,

                    metadata={

                        "trace_id":

                            trace.trace_id

                    },

                )




        except Exception as exc:


            logger.exception(

                "Agent runtime failed"

            )


            metrics.increment(

                "runtime_errors_total"

            )


            return AgentResult.failure(

                error=build_error_info(exc)

            )




        finally:


            trace.finish()


            try:

                span_count = len(
                    trace.spans
                )

            except Exception:

                span_count = 0



            logger.info(

                "Trace completed",

                extra={

                    "trace_id":

                        trace.trace_id,


                    "duration_ms":

                        getattr(

                            trace,

                            "duration_ms",

                            0,

                        ),


                    "span_count":

                        span_count,

                },

            )