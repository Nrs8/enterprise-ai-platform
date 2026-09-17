# Changelog

## Current

### Enterprise Platform Hardening

- Hardened Docker runtime configuration.
- Added configurable LLM timeout.
- Added configurable retry count.
- Added configurable worker count.
- Added transient LLM retry handling.
- Added graceful worker shutdown.
- Added runtime error handling.
- Added authorization error handling.
- Added non-root Docker execution.
- Added container health check.

### Security and Governance

- Added user and tenant identity to `AgentContext`.
- Added permission checking.
- Added model policy enforcement.
- Added quota checking.
- Added budget checking.
- Added token estimation.
- Added audit logging.
- Added usage and cost tracking.
- Propagated identity through LLM execution.

### Task Execution

- Added asynchronous task API.
- Added in-memory task queue.
- Added task workers.
- Added task execution isolation.
- Added task ownership checks.
- Added task session creation through `MemoryManager`.
- Added user and tenant propagation through task execution.

### API Quality

- Added request validation.
- Added stable runtime/LLM error responses.
- Added chat identity propagation.
- Added API regression tests for chat and tasks.
- Added task ownership regression tests.

### Deployment

- Added Docker Compose deployment.
- Added Docker health check.
- Added environment configuration template.
- Stabilized Qwen connectivity for the Docker runtime.

## Test Baseline

Current API test coverage includes:

- Chat API
- Task API
- Customer API
- Ticket API
- Runtime error handling

The full project test baseline is currently 81 passing tests.