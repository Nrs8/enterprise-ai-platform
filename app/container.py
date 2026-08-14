"""
Application dependency container.

Responsible for creating and sharing
enterprise AI platform components.
"""


from app.llm.providers.qwen import QwenLLM
from app.llm.providers.fake import FakeLLM

from app.llm.router import ModelRouter
from app.llm.gateway import LLMGateway


from app.memory.session_manager import (
    InMemorySessionManager,
)


from app.prompt.builder import PromptBuilder


from knowledge.embedder import SimpleEmbedder
from knowledge.vector_store import InMemoryVectorStore
from knowledge.knowledge_base import KnowledgeBase


from app.tools.registry import ToolRegistry
from app.tools.calculator import CalculatorTool


from app.usage.tracker import UsageTracker
from app.usage.calculator import CostCalculator


from app.audit.logger import AuditLogger


from app.security.permission import PermissionChecker
from app.security.quota import QuotaChecker
from app.security.token import TokenEstimator
from app.security.budget import BudgetChecker


from app.runtime.runtime import AgentRuntime
from app.runtime.loop import AgentLoop


from app.runtime.steps.retrieve import RetrieveStep
from app.runtime.steps.llm import LLMStep
from app.runtime.steps.tool import ToolStep
from app.runtime.steps.governance_step import GovernanceStep


from app.agents.registry import AgentRegistry

from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.tool_agent import ToolAgent
from app.agents.supervisor import SupervisorAgent


from app.observability import tracer



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

        self.session_manager = (
            InMemorySessionManager()
        )


        #
        # Audit
        #

        self.audit_logger = (
            AuditLogger()
        )


        #
        # LLM Providers
        #

        self.qwen = QwenLLM()

        self.fake = FakeLLM()



        #
        # Model Router
        #

        self.model_router = ModelRouter(

            providers={

                "qwen": self.qwen,

                "fake": self.fake,

            }

        )



        #
        # Usage / FinOps
        #

        self.cost_calculator = (
            CostCalculator()
        )


        self.usage_tracker = UsageTracker(

            calculator=self.cost_calculator

        )



        #
        # Security
        #

        self.permission_checker = (
            PermissionChecker()
        )


        self.token_estimator = (
            TokenEstimator()
        )


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

            permission_checker=
                self.permission_checker,

            quota_checker=
                self.quota_checker,

            token_estimator=
                self.token_estimator,

            budget_checker=
                self.budget_checker,

            audit_logger=
                self.audit_logger,

        )



        #
        # LLM Gateway
        #

        self.llm_gateway = LLMGateway(

            router=self.model_router,

            usage_tracker=self.usage_tracker,

        )



        #
        # Prompt
        #

        self.prompt_builder = (
            PromptBuilder()
        )



        #
        # Knowledge Base
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
        # Agent Loop
        #

        self.agent_loop = AgentLoop(

            llm_step=self.llm_step,

            tool_step=self.tool_step,

            tracer=tracer,

        )



        #
        # Agent Registry
        #

        self.agent_registry = AgentRegistry()



        #
        # Knowledge Agent
        #

        self.knowledge_agent = KnowledgeAgent(

            retrieve_step=self.retrieve_step,

            llm_step=self.llm_step,

        )



        #
        # Tool Agent
        #

        self.tool_agent = ToolAgent(

            llm_step=self.llm_step,

            agent_loop=self.agent_loop,

        )



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

            registry=self.agent_registry,
            tracer=tracer,

        )



        #
        # Runtime
        #

        self.runtime = AgentRuntime(

            session_manager=self.session_manager,

            supervisor_agent=self.supervisor_agent,

            governance_step=self.governance_step,

            tracer=tracer,

        )