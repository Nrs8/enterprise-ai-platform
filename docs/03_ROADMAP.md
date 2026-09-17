# Roadmap

## Phase 1 — Core Platform

Status: Complete

- FastAPI application
- Agent Runtime
- Agent contracts
- Supervisor routing
- Agent Executor
- LLM Gateway
- Qwen provider
- Fake provider
- configuration management

## Phase 2 — AI Capabilities

Status: Complete

- Knowledge base
- Retrieval
- Vector search
- Tool calling
- Specialized agents
- Prompt construction
- Memory

## Phase 3 — Enterprise Runtime

Status: Complete

- Planning
- Workflow execution
- MCP integration
- Customer domain
- Ticket domain
- Async task queue
- Task workers

## Phase 4 — Governance and Observability

Status: Complete

- Permission checking
- Model policy
- Token estimation
- Quotas
- Budgets
- Usage tracking
- Cost calculation
- Audit logging
- Metrics
- Tracing

## Phase 5 — Reliability and Deployment

Status: Complete

- Timeout handling
- Transient-error retry
- LLM error handling
- Worker failure isolation
- Graceful shutdown
- Docker image
- Docker Compose
- Container health check
- Non-root container execution

## Phase 6 — Quality and Documentation

Status: In Progress

- API regression tests
- Identity propagation tests
- Task ownership tests
- README update
- Architecture documentation
- Coding standards
- Changelog
- Final repository review

## Future Production Evolution

These items are intentionally outside the current local/MVP scope:

- Real authentication and identity provider integration
- Durable distributed task queue
- Distributed task state
- Persistent production database
- Distributed vector database
- External observability stack
- Horizontal scaling
- Production secret management
- Multi-instance coordination
- Production-grade MCP multi-tenancy

These should be introduced only when deployment requirements justify them.