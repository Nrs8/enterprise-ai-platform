"""
Agent runtime execution context.

Stores all runtime state shared
between agents and execution steps.


Responsibilities:

- Runtime identity
- Conversation memory
- LLM execution messages
- Tool execution state
- Retrieval context
- Planning state
- Workflow state
- Runtime metadata


Context is the shared state container.

It does NOT:

- call LLM
- execute tools
- persist memory
"""



from __future__ import annotations



from typing import Any



from app.memory.models import (
    Message as MemoryMessage,
)



from app.llm.models import (
    Message as LLMMessage,
    LLMResponse,
    ToolCall,
)



from app.planning.models import (
    ExecutionPlan,
)







class AgentContext:
    """
    Stores runtime execution state.


    Shared between:


    Runtime

        |

        v


    Supervisor

        |

        v


    Planner

        |

        v


    Workflow

        |

        v


    Agents

        |

        v


    Execution Steps

    """






    def __init__(

        self,

        session_id: str,

        input: str,

        model: str = "qwen",

        user_id: str = "anonymous",

        tenant_id: str = "default",

        trace=None,

    ) -> None:



        #
        # Identity
        #

        self.session_id = session_id

        self.user_id = user_id

        self.tenant_id = tenant_id







        #
        # User Input
        #

        self.input = input







        #
        # Model
        #

        self.model = model







        #
        # Observability
        #

        self.trace = trace







        #
        # Persistent Memory
        #

        self.session = None



        self.history: list[
            MemoryMessage
        ] = []



        self.memory_context: dict[
            str,
            Any
        ] = {}








        #
        # LLM Runtime Messages
        #

        self.messages: list[
            LLMMessage
        ] = []








        #
        # Retrieval Context
        #

        self.knowledge_context: str = ""








        #
        # LLM Response
        #

        self.llm_response: (
            LLMResponse | None
        ) = None








        #
        # Tool State
        #

        self.tool_results: list[Any] = []








        #
        # Planning State
        #

        self.plan: (
            ExecutionPlan | None
        ) = None



        #
        # Supervisor Decision
        #

        self.decision = None







        #
        # Workflow State
        #

        #
        # Filled by AgentRuntime
        #

        self.workflow_state = None







        #
        # Runtime Metadata
        #

        self.metadata: dict[
            str,
            Any
        ] = {}








        #
        # Workflow Variables
        #

        self.variables: dict[
            str,
            Any
        ] = {}








        #
        # Final Response
        #

        self.response: (
            str | None
        ) = None










    def load_history(

        self,

        messages: list[MemoryMessage],

    ) -> None:
        """
        Load persistent conversation history.


        Memory layer keeps
        MemoryMessage objects.


        PromptBuilder converts them
        into LLM messages.
        """



        self.history = messages



        #
        # Reset temporary messages
        #

        self.messages = []










    def set_memory_context(

        self,

        context: dict[str, Any],

    ) -> None:
        """
        Store injected memory context.
        """

        self.memory_context = context










    def set_plan(

        self,

        plan: ExecutionPlan,

    ) -> None:
        """
        Store generated execution plan.
        """

        self.plan = plan










    def set_workflow_state(

        self,

        state: Any,

    ) -> None:
        """
        Store workflow runtime state.
        """

        self.workflow_state = state










    def add_user_message(

        self,

        content: str,

    ) -> None:
        """
        Add user message into
        runtime LLM messages.
        """

        self.messages.append(

            LLMMessage(

                role="user",

                content=content,

            )

        )










    def add_assistant_message(

        self,

        content: str,

        tool_calls: list[ToolCall] | None = None,

    ) -> None:
        """
        Add assistant tool request.
        """

        self.messages.append(

            LLMMessage(

                role="assistant",

                content=content,

                tool_calls=(

                    tool_calls

                    or []

                ),

            )

        )










    def add_tool_message(

        self,

        content: str,

        tool_call_id: str,

    ) -> None:
        """
        Add tool result message.
        """

        self.messages.append(

            LLMMessage(

                role="tool",

                content=content,

                tool_call_id=tool_call_id,

            )

        )










    def set_llm_response(

        self,

        response: LLMResponse,

    ) -> None:
        """
        Store latest LLM response.
        """

        self.llm_response = response










    def add_tool_result(

        self,

        result: Any,

    ) -> None:
        """
        Store tool execution output.
        """

        self.tool_results.append(

            result

        )










    def set_response(

        self,

        response: str,

    ) -> None:
        """
        Store final assistant response.
        """

        self.response = response