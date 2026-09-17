# Enterprise AI Agent Platform — Project Context

## Goal

Build a production-oriented Enterprise AI Agent Platform that demonstrates practical AI engineering and platform architecture.

The project is intended to demonstrate:

- AI agent orchestration
- LLM infrastructure
- enterprise governance
- tool and MCP integration
- memory and RAG
- asynchronous execution
- reliability
- observability
- domain integration
- containerized deployment

## Target Roles

- AI Engineer
- Enterprise AI Platform Engineer
- AI Application Engineer
- AI Architect

## Design Philosophy

The project favors a modular monolith with explicit boundaries over premature distributed-system complexity.

The system should remain understandable, testable, and deployable on local hardware while preserving interfaces that can later support distributed infrastructure.

## Architecture Principles

- Separation of Concerns
- SOLID
- Dependency Inversion
- Dependency Injection
- Explicit interfaces
- Layered architecture
- Testability
- Production-first engineering
- Incremental evolution
- Failure isolation

## Runtime Principle

The runtime is the orchestration layer.

It coordinates:

- request context
- governance
- memory
- supervisor routing
- planning
- workflow execution
- agent execution

The runtime should not contain business-specific domain logic or directly implement provider-specific LLM behavior.

## Responsibility Boundaries

### Runtime

Coordinates execution.

### Agents

Perform agent-specific reasoning and behavior.

### LLM Gateway

Provides an abstraction over LLM providers.

### Providers

Handle provider-specific API communication.

### Domain Services

Own customer and ticket business logic.

### Security

Owns permission, policy, quota, budget and token governance.

### Infrastructure

Provides memory, MCP, tools, observability, resilience and persistence mechanisms.

## Teaching / Development Style

The project is developed using a Principal AI Architect mindset.

For changes:

1. Review existing code first.
2. Identify the exact boundary affected.
3. Specify the file to change.
4. Specify the action.
5. Explain the reason.
6. Avoid unnecessary rearchitecture.
7. Preserve existing interfaces unless a change is justified.
8. Add regression coverage for important behavior.