"""
Application dependency container.

Responsible for creating and sharing
enterprise AI platform components.
"""


#
# LLM
#

from app.llm.providers.qwen import QwenLLM
from app.llm.providers.fake import FakeLLM

from app.llm.router import ModelRouter
from app.llm.gateway import LLMGateway


#
# Memory
#

from app.memory.manager import MemoryManager

from app.memory.window import ContextWindow

from app.memory.context_builder import (
    ContextBuilder,
)

from app.memory.providers.file_store import (
    FileMemoryStore,
)

from app.memory.repository import (
    FileConversationRepository,
    FileUserMemoryRepository,
)


#
# Prompt
#

from app.prompt.builder import (
    PromptBuilder,
)


#
# Knowledge
#

from knowledge.embedder import (
    SimpleEmbedder,
)

from knowledge.vector_store import (
    InMemoryVectorStore,
)

from knowledge.knowledge_base import (
    KnowledgeBase,
)


#
# Tools
#

from app.tools.registry import (
    ToolRegistry,
)

from app.tools.calculator import (
    CalculatorTool,
)


#
# MCP
#

from app.mcp.adapter import (
    MCPToolAdapter,
)

from app.mcp.server import (
    MCPServer,
)

from app.mcp.factory import (
    create_mcp_bridge,
)


#
# Usage
#

from app.usage.tracker import (
    UsageTracker,
)

from app.usage.calculator import (
    CostCalculator,
)


#
# Audit
#

from app.audit.logger import (
    AuditLogger,
)


#
# Security
#

from app.security.permission import (
    PermissionChecker,
)

from app.security.quota import (
    QuotaChecker,
)

from app.security.token import (
    TokenEstimator,
)

from app.security.budget import (
    BudgetChecker,
)


#
# Runtime
#

from app.runtime.runtime import (
    AgentRuntime,
)

from app.runtime.executor.tool_calling_executor import (
    ToolCallingExecutor,
)


#
# Agent
#

from app.agents.executor import (
    AgentExecutor,
)

from app.agents.registry import (
    AgentRegistry,
)

from app.agents.knowledge_agent import (
    KnowledgeAgent,
)

from app.agents.tool_agent import (
    ToolAgent,
)

from app.agents.supervisor import (
    SupervisorAgent,
)


#
# Runtime Steps
#

from app.runtime.steps.retrieve import (
    RetrieveStep,
)

from app.runtime.steps.llm import (
    LLMStep,
)

from app.runtime.steps.tool import (
    ToolStep,
)

from app.runtime.steps.governance_step import (
    GovernanceStep,
)


#
# Workflow
#

from app.workflow.engine import (
    WorkflowEngine,
)

from app.workflow.executors.agent_executor import (
    AgentWorkflowExecutor,
)


#
# Planning
#

from app.planning.planner import (
    SimplePlanner,
)

from app.planning.executor import (
    PlanExecutor,
)

from app.planning.workflow_builder import (
    WorkflowBuilder,
)


#
# Observability
#

from app.observability import (
    tracer,
)



class Container:
    """
    Application dependency container.

    Creates and wires all enterprise AI
    platform components.
    """


    def __init__(self) -> None:


        #
        # Memory
        #

        self.memory_store = FileMemoryStore()


        self.conversation_repository = (
            FileConversationRepository(
                self.memory_store
            )
        )


        self.user_memory_repository = (
            FileUserMemoryRepository(
                self.memory_store
            )
        )


        self.memory_manager = MemoryManager(
            conversation_repository=(
                self.conversation_repository
            ),
            user_memory_repository=(
                self.user_memory_repository
            ),
        )



        #
        # Context
        #

        self.context_window = ContextWindow(
            max_messages=20
        )


        self.context_builder = ContextBuilder(
            context_window=self.context_window
        )



        #
        # Audit
        #

        self.audit_logger = AuditLogger()



        #
        # LLM
        #

        self.qwen = QwenLLM()

        self.fake = FakeLLM()


        self.model_router = ModelRouter(
            providers={
                "qwen": self.qwen,
                "fake": self.fake,
            }
        )



        #
        # Usage
        #

        self.cost_calculator = CostCalculator()


        self.usage_tracker = UsageTracker(
            calculator=self.cost_calculator
        )



        #
        # Security
        #

        self.permission_checker = PermissionChecker()

        self.token_estimator = TokenEstimator()


        self.quota_checker = QuotaChecker(
            usage_tracker=self.usage_tracker
        )


        self.budget_checker = BudgetChecker(
            usage_tracker=self.usage_tracker
        )



        #
        # Governance
        #

        self.governance_step = GovernanceStep(
            permission_checker=self.permission_checker,
            quota_checker=self.quota_checker,
            token_estimator=self.token_estimator,
            budget_checker=self.budget_checker,
            audit_logger=self.audit_logger,
        )



        #
        # Gateway
        #

        self.llm_gateway = LLMGateway(
            router=self.model_router,
            usage_tracker=self.usage_tracker,
        )



        #
        # Prompt
        #

        self.prompt_builder = PromptBuilder()



        #
        # Knowledge
        #

        self.knowledge_base = KnowledgeBase(
            embedder=SimpleEmbedder(),
            vector_store=InMemoryVectorStore(),
        )



        #
        # Tools
        #

        self.tool_registry = ToolRegistry()


        self.tool_registry.register(
            CalculatorTool()
        )



        #
        # MCP Runtime Integration
        #

        self.mcp_adapter = MCPToolAdapter(
            self.tool_registry
        )


        self.mcp_server = MCPServer(
            self.mcp_adapter
        )


        self.mcp_bridge = create_mcp_bridge(
            tool_registry=self.tool_registry,
            server_name="local",
            server=self.mcp_server,
        )


        #
        # Runtime Steps
        #

        self.retrieve_step = RetrieveStep(
            self.knowledge_base
        )


        self.llm_step = LLMStep(
            llm_gateway=self.llm_gateway,
            prompt_builder=self.prompt_builder,
            tool_registry=self.tool_registry,
        )


        self.tool_step = ToolStep(
            tool_registry=self.tool_registry,
            permission_checker=self.permission_checker,
        )



        #
        # Tool Calling Executor
        #

        self.tool_calling_executor = (
            ToolCallingExecutor(
                llm_step=self.llm_step,
                tool_step=self.tool_step,
                tracer=tracer,
            )
        )



        #
        # Agent Lifecycle Executor
        #

        self.agent_executor = AgentExecutor()



        #
        # Agents
        #

        self.knowledge_agent = KnowledgeAgent(

            retrieve_step=self.retrieve_step,

            llm_step=self.llm_step,

        )


        self.tool_agent = ToolAgent(

            tool_calling_executor=(
                self.tool_calling_executor
            ),

        )



        #
        # Agent Registry
        #

        self.agent_registry = AgentRegistry()


        self.agent_registry.register(
            self.knowledge_agent
        )


        self.agent_registry.register(
            self.tool_agent
        )



        #
        # Supervisor
        #

        self.supervisor_agent = SupervisorAgent(

            tracer=tracer,

        )



        #
        # Workflow Engine
        #

        self.workflow_engine = WorkflowEngine()



        self.agent_workflow_executor = (
            AgentWorkflowExecutor(

                self.agent_registry

            )
        )


        self.workflow_engine.register_executor(

            "tool",

            self.agent_workflow_executor,

        )


        self.workflow_engine.register_executor(

            "knowledge",

            self.agent_workflow_executor,

        )



        #
        # Planning
        #

        self.workflow_builder = WorkflowBuilder()


        self.planner = SimplePlanner()



        self.plan_executor = PlanExecutor(

            workflow_engine=self.workflow_engine,

            workflow_builder=self.workflow_builder,

        )



        #
        # Agent Runtime
        #

        self.runtime = AgentRuntime(

            memory_manager=self.memory_manager,

            context_builder=self.context_builder,

            supervisor_agent=self.supervisor_agent,

            agent_registry=self.agent_registry,

            agent_executor=self.agent_executor,

            governance_step=self.governance_step,

            tracer=tracer,

        )