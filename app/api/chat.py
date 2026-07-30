from fastapi import APIRouter
from pydantic import BaseModel

from app.llm.gateway import LLMGateway
from app.memory.session_manager import InMemorySessionManager
from app.prompt.builder import PromptBuilder
from app.runtime.runtime import AgentRuntime
from app.task.manager import InMemoryTaskManager
from app.task.executor import TaskExecutor

from knowledge.chunker import TextChunker
from knowledge.document_loader import DocumentLoader
from knowledge.embedder import SimpleEmbedder
from knowledge.knowledge_base import KnowledgeBase
from knowledge.vector_store import InMemoryVectorStore

from app.tools.calculator import CalculatorTool
from app.tools.registry import ToolRegistry
from app.task.queue import InMemoryTaskQueue
from app.observability import tracer
router = APIRouter()


# Initialize core dependencies.
llm_gateway = LLMGateway()

session_manager = InMemorySessionManager()

prompt_builder = PromptBuilder()


# Initialize the knowledge base.
knowledge_base = KnowledgeBase(
    embedder=SimpleEmbedder(),
    vector_store=InMemoryVectorStore(),
)


# Load knowledge documents.
document_loader = DocumentLoader()

documents = document_loader.load_directory(
    "knowledge_data/documents"
)


# Chunk and index documents.
chunker = TextChunker()

for document in documents:
    chunks = chunker.split(document)

    knowledge_base.add_document(
        document=document,
        chunks=chunks,
    )


# Initialize tools.
tool_registry = ToolRegistry()

tool_registry.register(
    CalculatorTool()
)


# Compose the AgentRuntime.
runtime = AgentRuntime(
    llm_gateway=llm_gateway,
    session_manager=session_manager,
    prompt_builder=prompt_builder,
    knowledge_base=knowledge_base,
    tool_registry=tool_registry,
)


# Initialize task execution layer.
task_manager = InMemoryTaskManager()

task_executor = TaskExecutor(
    task_manager=task_manager,
    agent_runtime=runtime,
)
task_queue = InMemoryTaskQueue()

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Create and execute an Agent task.
    """

    session_id = request.session_id

    if session_id is None:
        session = session_manager.create_session()
        session_id = session.session_id

    # Create a task.
    task = task_manager.create_task(
        session_id=session_id,
        input=request.message,
    )
    trace = tracer.start_trace()
    # Execute the task through the AgentRuntime.
    await task_executor.execute(
        task_id=task.id,
    )
    trace.finish()
    # Get the final task state.
    completed_task = task_manager.get_task(
        task_id=task.id,
    )

    return {
        "session_id": session_id,
        "task_id": task.id,
        "status": completed_task.status,
        "response": completed_task.result,
    }