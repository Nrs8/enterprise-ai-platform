# Enterprise AI Platform

A production-oriented enterprise AI agent platform built with FastAPI and Python.

The project demonstrates how to structure an AI application as a modular monolith with explicit boundaries between API, runtime orchestration, agents, LLM infrastructure, tools, memory, workflow, security/governance, observability, domain services, and asynchronous task execution.

## Core Capabilities

- Agent Runtime orchestration
- Supervisor-based agent routing
- Specialized agents
- LLM Gateway abstraction
- OpenAI-compatible Qwen provider
- RAG / knowledge retrieval
- Tool calling
- MCP integration
- Conversation memory
- Async task queue and workers
- Workflow execution
- Security and governance
- Permission and model policy
- Quota and budget controls
- Token estimation
- Usage tracking and cost calculation
- Audit logging
- Request tracing and metrics
- Retry and timeout resilience
- Customer and ticket domain services
- Evaluation support
- Docker deployment

## Architecture

```text
Client
  |
  v
FastAPI API
  |
  v
AgentRuntime
  |
  +--> Governance
  |
  +--> Memory / Context
  |
  +--> Supervisor
          |
          v
      AgentExecutor
          |
          +--> KnowledgeAgent
          +--> ToolAgent
          +--> CustomerServiceAgent
          |
          v
      Agent Steps / Workflow
          |
          v
      LLM Gateway
          |
          v
      Qwen Provider
          |
          v
      OpenAI-Compatible LLM API