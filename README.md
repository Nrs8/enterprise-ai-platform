# Enterprise AI Platform

Production-grade enterprise AI agent platform built with FastAPI.

## Features

* Agent Runtime orchestration
* LLM Gateway abstraction
* RAG knowledge retrieval
* Tool Calling
* Session Memory
* Task Queue & Workers
* Observability / Request Tracing

## Tech Stack

* Python
* FastAPI
* AsyncIO
* OpenAI-compatible LLM API
* Vector Search
* Modular Monolith Architecture

## Project Structure

```
app/
knowledge/
tests/
```

## Run

```bash
uvicorn app.main:app --reload
```
