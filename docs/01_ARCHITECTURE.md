# Architecture

## System Overview

The platform is implemented as a modular monolith.

```text
Client
  |
  v
FastAPI
  |
  v
AgentRuntime
  |
  +--> Governance
  +--> Memory
  +--> Context
  +--> Supervisor
  +--> Planning / Workflow
  |
  v
AgentExecutor
  |
  +--> KnowledgeAgent
  +--> ToolAgent
  +--> CustomerServiceAgent
  |
  v
Agent Steps
  |
  +--> Retrieval
  +--> LLM
  +--> Tool Calling
  |
  v
LLMGateway
  |
  v
Qwen Provider
  |
  v
External LLM API