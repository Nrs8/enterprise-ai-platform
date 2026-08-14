from app.memory.models import Message
from app.llm.models import LLMResponse


class AgentContext:
    """
    Stores runtime execution state.

    The context is shared between
    different execution steps.
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


        self.session_id = session_id
        self.user_id = user_id
        self.tenant_id = tenant_id

        # Original user input
        self.input = input


        # Selected model/provider
        self.model = model


        # Observability trace
        self.trace = trace


        # Conversation session
        self.session = None


        # Messages sent to LLM
        self.messages: list[Message] = []


        # RAG retrieved knowledge
        self.knowledge_context: str = ""


        # LLM response
        self.llm_response: LLMResponse | None = None


        # Tool execution results
        self.tool_results: list = []


        # Final assistant answer
        self.response: str | None = None