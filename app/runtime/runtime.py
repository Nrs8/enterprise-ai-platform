"""
Agent runtime responsible for conversation orchestration.
"""

import logging

from app.llm.gateway import LLMGateway
from app.llm.models import ToolResult
from app.memory.models import Message
from app.memory.session_manager import InMemorySessionManager
from app.prompt.builder import PromptBuilder
from app.tools.registry import ToolRegistry
from knowledge.knowledge_base import KnowledgeBase
from app.observability import tracer
from app.observability.models import Trace
logger = logging.getLogger(__name__)


class AgentRuntime:
    """
    Coordinates conversation flow between memory and LLM services.
    """

    def __init__(
        self,
        llm_gateway: LLMGateway,
        session_manager: InMemorySessionManager,
        prompt_builder: PromptBuilder,
        knowledge_base: KnowledgeBase,
        tool_registry: ToolRegistry,
        tracer=tracer,
    ) -> None:
        """
        Initialize agent runtime.

        Args:
            llm_gateway:
                Handles communication with LLM providers.

            session_manager:
                Handles conversation session storage.

            prompt_builder:
                Builds prompts from system instructions, history,
                the current user message, and knowledge context.

            knowledge_base:
                Provides relevant knowledge context.

            tool_registry:
                Stores and resolves available tools.
        """

        self._llm_gateway = llm_gateway
        self._session_manager = session_manager
        self._prompt_builder = prompt_builder
        self._knowledge_base = knowledge_base
        self._tool_registry = tool_registry
        self.tracer = tracer

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> ToolResult:
        """
        Execute a registered tool.
        """

        try:
            result = await self._tool_registry.execute(
                tool_name=tool_name,
                arguments=arguments,
            )

            return ToolResult(
                success=True,
                content=str(result),
            )

        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
        
    async def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:
        """
        Process one user message.

        Steps:
            1. Retrieve existing session.
            2. Search relevant knowledge.
            3. Build prompt.
            4. Send conversation to LLM.
            5. Execute tool if requested.
            6. Store user message.
            7. Store assistant response.
            8. Return assistant response.

        Args:
            session_id:
                Conversation identifier.

            message:
                User input text.

        Returns:
            Assistant response.
        """
        trace = self.tracer.start_trace()

        with self.tracer.span(
            trace,
            "agent_runtime",
            {
                "session_id": session_id
            },
        ):

            # Load existing conversation session.
            session = self._session_manager.get_session(
                session_id
            )

            logger.info(
                "Loaded conversation session",
                extra={
                    "session_id": session_id,
                    "message_count": len(session.messages),
                },
            )

            # Retrieve relevant knowledge.
            relevant_chunks = self._knowledge_base.search(
                query=message,
                top_k=3,
            )

            knowledge_context = "\n\n".join(
                chunk.content
                for chunk in relevant_chunks
            )

            # Build prompt.
            messages = self._prompt_builder.build(
                history=session.messages,
                user_message=message,
                knowledge_context=knowledge_context,
            )

            # Generate LLM response.
            max_iterations = 10

            for _ in range(max_iterations):
                with self.tracer.span(
                trace,
                "llm_call",
                ):
                    response = await self._llm_gateway.generate(
                        messages=messages,
                        tools=self._tool_registry.get_schemas(),
                    )

                # Return final answer when no tool call is requested.
                if not response.tool_calls:
                    assistant_response = response.content or ""
                    break

                # Add LLM Tool Call to the current context.
                messages.append(
                    Message(
                        role="assistant",
                        content=response.content,
                        tool_calls=response.tool_calls,
                    )
                )

                # Execute every requested tool.
                for tool_call in response.tool_calls:

                    with self.tracer.span(
                        trace,
                        "tool_call",
                        {
                            "tool": tool_call.name,
                        },
                    ):
                        tool_result = await self.execute_tool(
                            tool_name=tool_call.name,
                            arguments=tool_call.arguments,
                        )

                    if tool_result.success:
                        tool_content = tool_result.content or ""
                    else:
                        tool_content = (
                            f"Tool execution failed: "
                            f"{tool_result.error}"
                        )

                    # Add each tool result to the current context.
                    messages.append(
                        Message(
                            role="tool",
                            content=tool_content,
                            tool_call_id=tool_call.id,
                        )
                    )

            else:
                raise RuntimeError(
                    "Agent loop exceeded maximum iterations."
                )

            # Store user message.
            user_message = Message(
                role="user",
                content=message,
            )

            self._session_manager.add_message(
                session_id,
                user_message,
            )

            logger.info(
                "User message stored",
                extra={
                    "session_id": session_id,
                },
            )

            # Store assistant response.
            assistant_message = Message(
                role="assistant",
                content=assistant_response,
            )

            self._session_manager.add_message(
                session_id,
                assistant_message,
            )

            logger.info(
                "Assistant message stored",
                extra={
                    "session_id": session_id,
                },
            )
        logger.info(
            "Trace completed",
            extra={
                "trace_id": trace.trace_id,
                "span_count": len(trace.spans),
            },
        )
        trace.finish()

        print(
            f"TRACE: {trace.trace_id} {trace.duration_ms:.2f}ms"
        )

        for span in trace.spans:
            print(
                f"SPAN: {span.name} {span.duration_ms:.2f}ms {span.attributes}"
            )

        return assistant_response