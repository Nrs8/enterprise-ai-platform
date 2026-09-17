# Coding Standard

## General Principles

Code should prioritize:

- clarity
- explicit dependencies
- testability
- small responsibilities
- stable interfaces
- predictable failure behavior

## Architecture

Follow separation of concerns.

API handlers should not contain:

- agent reasoning
- provider-specific LLM logic
- domain business rules
- complex workflow orchestration

Use the appropriate layer instead.

## Dependency Injection

Dependencies should be constructed in the application container where practical.

Components should receive their dependencies explicitly.

Avoid hidden global construction of core services.

## Runtime

The runtime coordinates execution.

Do not move business logic into `AgentRuntime` merely for convenience.

## Agents

Agents implement explicit contracts.

Agent-specific behavior belongs inside agents or their supporting services.

## LLM

Provider-specific code belongs under the LLM infrastructure layer.

Application code should use `LLMGateway` rather than directly constructing provider clients.

## Error Handling

Use domain-specific exceptions where they improve clarity.

Do not catch broad exceptions unless the boundary requires failure isolation.

At infrastructure boundaries:

- log useful diagnostic information
- avoid exposing secrets
- return stable API errors
- preserve the original exception through exception chaining where appropriate

## Reliability

Retries must be limited to transient failures.

Do not retry deterministic validation or authorization failures.

Timeouts must be explicit and configurable.

## Security

Identity should flow through execution context.

Authorization decisions should be centralized in security components rather than duplicated across agents.

Do not log secrets, API keys, tokens, or sensitive request content unnecessarily.

## API

Use Pydantic models for request validation.

Validate:

- required values
- string lengths
- supported values
- request shape

API handlers should remain thin.

## Testing

Tests should verify behavior at the appropriate boundary.

Prefer:

- unit tests for isolated components
- API tests for HTTP contracts
- integration tests for component interaction
- end-to-end tests only where real integration behavior is important

Network-dependent tests should not run unintentionally during normal test collection.

## Naming

Use explicit names that communicate responsibility.

Examples:

- `AgentRuntime`
- `LLMGateway`
- `TaskExecutor`
- `PermissionChecker`
- `MemoryManager`

Avoid vague names such as:

- `Manager`
- `Helper`
- `Utils`

unless the responsibility is genuinely clear from context.

## Change Discipline

Before changing architecture:

1. inspect the existing implementation
2. identify the actual boundary
3. determine whether the requirement can be satisfied locally
4. preserve existing contracts where possible
5. add regression coverage
6. avoid speculative abstractions

## Documentation

Documentation should describe the implemented system.

Do not document planned architecture as if it already exists.

When architecture changes, update:

- README
- architecture documentation
- roadmap/current sprint where relevant
- changelog
- tests