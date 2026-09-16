"""
Chat API endpoint.
"""

import logging
from uuid import uuid4

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)
from pydantic import BaseModel, Field

from app.resilience.exceptions import LLMError
from app.observability.metrics import metrics


logger = logging.getLogger(__name__)

router = APIRouter()


# =========================
# API Models
# =========================


class ChatRequest(BaseModel):
    """
    Chat request payload.
    """

    message: str = Field(
        min_length=1,
        max_length=10000,
    )

    model: str = Field(
        default="qwen",
        min_length=1,
        max_length=100,
    )

    session_id: str | None = None

    user_id: str = Field(
        default="anonymous",
        min_length=1,
        max_length=100,
    )

    tenant_id: str = Field(
        default="default",
        min_length=1,
        max_length=100,
    )


# =========================
# Chat Endpoint
# =========================


@router.post("/chat")
async def chat(
    http_request: Request,
    request: ChatRequest,
):
    """
    Execute AI agent conversation.
    """

    metrics.increment(
        "chat_requests"
    )

    logger.info(
        "Metrics snapshot: %s",
        metrics.snapshot(),
    )

    #
    # Get application container
    #

    container = (
        http_request
        .app
        .state
        .container
    )

    runtime = container.runtime

    if runtime is None:
        raise HTTPException(
            status_code=503,
            detail="AI runtime is unavailable",
        )

    #
    # Persistent Memory Session
    #

    session_id = request.session_id

    if session_id is None:
        session_id = str(uuid4())

        container.memory_manager.create_conversation(
            session_id=session_id,
            user_id=request.user_id,
        )

    try:

        response = await runtime.chat(
            session_id=session_id,
            message=request.message,
            model=request.model,
            user_id=request.user_id,
            tenant_id=request.tenant_id,
        )

        return {
            "session_id": session_id,
            "model": request.model,
            "response": response,
        }

    except LLMError as exc:

        logger.error(
            "LLM request failed: %s",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=503,
            detail="LLM service is temporarily unavailable",
        ) from exc

    except Exception:

        logger.exception(
            "Chat request failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )
