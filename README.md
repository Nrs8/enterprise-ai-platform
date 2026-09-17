# Enterprise AI Platform

A production-oriented enterprise AI agent platform built with Python and FastAPI.

The project demonstrates how to structure an AI application as a modular monolith with explicit boundaries between API, runtime orchestration, agents, LLM infrastructure, tools, memory, workflow, security/governance, observability, domain services, and asynchronous task execution.

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
  |      +--> Permission
  |      +--> Model Policy
  |      +--> Quota
  |      +--> Budget
  |      +--> Token Estimation
  |      +--> Audit
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
          +--> Retrieval
          +--> Tool Calling
          +--> LLM
          |
          v
      LLM Gateway
          |
          v
      Qwen Provider
          |
          v
      OpenAI-Compatible LLM API
```

The runtime is responsible for orchestration rather than provider-specific LLM behavior or domain business logic.

## Core Capabilities

### Agent Platform

* Agent Runtime orchestration
* Supervisor-based routing
* Explicit agent contracts
* Agent Executor boundary
* Specialized agents
* Workflow execution
* Planning

### AI Infrastructure

* LLM Gateway abstraction
* OpenAI-compatible provider interface
* Qwen provider
* Fake provider for testing
* RAG / knowledge retrieval
* Vector search
* Tool calling
* MCP integration
* Conversation memory

### Enterprise Governance

* Permission checking
* Model policy enforcement
* Token estimation
* Quota controls
* Budget controls
* Usage tracking
* Cost calculation
* Audit logging
* User and tenant context propagation

### Reliability

* Configurable LLM timeout
* Transient-error retry
* LLM error handling
* Worker failure isolation
* Graceful worker shutdown
* API error handling
* Container health checks

### Domain and Application Services

* Customer domain service
* Ticket domain service
* Asynchronous task execution
* Task ownership checks
* Request tracing
* Metrics
* Evaluation support

### Deployment

* Docker
* Docker Compose
* Non-root container execution
* Environment-based configuration
* Local development workflow

## Project Structure

```text
app/
├── agents/          # Specialized AI agents
├── api/             # FastAPI routes
├── config/          # Application configuration
├── domain/          # Customer and ticket business domains
├── evaluation/      # Evaluation utilities
├── llm/             # LLM gateway and providers
├── memory/          # Conversation and user memory
├── mcp/             # MCP integration
├── observability/   # Metrics, tracing and audit
├── resilience/      # Retry and timeout handling
├── runtime/         # Agent orchestration
├── security/        # Permission and governance
├── task/            # Async task queue and workers
├── tools/           # Tool implementations
└── main.py          # FastAPI application entry point

knowledge/           # Knowledge sources
knowledge_data/      # Retrieval data
docker/              # Docker image definition
docs/                # Architecture and project documentation
tests/               # Automated tests
compose.yaml         # Docker Compose deployment
.env.example         # Environment configuration template
```

## API

The current API surface includes:

| Method | Endpoint                      | Purpose                       |
| ------ | ----------------------------- | ----------------------------- |
| GET    | `/health`                     | Service health                |
| POST   | `/chat`                       | Synchronous agent interaction |
| POST   | `/tasks`                      | Create asynchronous task      |
| GET    | `/tasks/{task_id}`            | Query task status             |
| GET    | `/customers/{customer_id}`    | Retrieve customer             |
| GET    | `/tickets/{ticket_id}`        | Retrieve ticket               |
| POST   | `/tickets`                    | Create ticket                 |
| PATCH  | `/tickets/{ticket_id}/status` | Update ticket status          |
| GET    | `/usage`                      | Usage information             |
| GET    | `/audit`                      | Audit records                 |

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Running Locally

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` from `.env.example` and provide the required LLM configuration.

Start the application:

```powershell
uvicorn app.main:app --reload
```

Then open:

```text
http://localhost:8000/docs
```

## Docker

Build and start the platform:

```powershell
docker compose up --build -d
```

Check the container:

```powershell
docker compose ps
```

Check service health:

```text
http://localhost:8000/health
```

Open the API documentation:

```text
http://localhost:8000/docs
```

Stop the service:

```powershell
docker compose down
```

The Docker image:

* uses Python 3.14 slim
* runs as a non-root user
* exposes port 8000
* includes a container health check
* supports graceful SIGTERM shutdown
* uses environment-based configuration

## Testing

The current project test baseline is **85 passing tests**.

Run the full test suite:

```powershell
pytest -q
```

Run API tests:

```powershell
pytest tests/api -v
```

Network-dependent provider tests are kept separate from normal test collection so the standard test suite remains deterministic.

## Security and Identity

The platform propagates `user_id` and `tenant_id` through the execution context and uses them for governance, quota, audit, task ownership, and downstream execution.

The current implementation uses an application-level identity model.

`user_id` and `tenant_id` supplied through API requests are **not a replacement for real authentication**.

A production deployment would integrate an external identity provider and derive authenticated identity from verified credentials or tokens rather than trusting request fields directly.

## Production Evolution

The current system is intentionally implemented as a local, testable modular monolith.

Future production evolution may include:

* Real authentication and identity provider integration
* Durable distributed task queue
* Persistent production database
* Distributed task state
* Distributed vector database
* External observability stack
* Horizontal scaling
* Production secret management
* Multi-instance coordination
* Production-grade MCP multi-tenancy

These components should be introduced when actual deployment requirements justify them.

## Engineering Principles

The project follows:

* Separation of Concerns
* SOLID
* Dependency Inversion
* Dependency Injection
* Explicit interfaces
* Layered architecture
* Testability
* Production-oriented engineering
* Failure isolation
* Incremental evolution

The runtime coordinates execution. Agents own agent-specific behavior. The LLM Gateway abstracts providers. Domain services own business logic. Infrastructure components provide memory, tools, MCP, persistence, observability, and resilience.

## Documentation

Additional documentation:

* `docs/00_PROJECT_CONTEXT.md` — project goals and architectural principles
* `docs/01_ARCHITECTURE.md` — system architecture
* `docs/03_ROADMAP.md` — completed phases and future evolution
* `docs/04_CURRENT_SPRINT.md` — coding standards
* `docs/05_CHANGELOG.md` — project changes

## Project Status

The core platform implementation is complete for the current local/MVP scope.

The project has been validated through automated tests, Docker execution, API integration tests, asynchronous task execution, governance checks, and Qwen integration.

The current focus is portfolio presentation, deployment documentation, and interview readiness rather than adding unnecessary platform complexity.
