"""
Chat API endpoint.
"""

import logging

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from pydantic import BaseModel

from app.resilience.exceptions import LLMError

from app.observability.metrics import metrics


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - %(name)s - "
        "%(levelname)s - %(message)s"
    ),
)


logger = logging.getLogger(__name__)


router = APIRouter()


# =========================
# API Models
# =========================

class ChatRequest(BaseModel):
    """
    Chat request payload.
    """

    message: str = "hello"

    model: str = "qwen"



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

        raise RuntimeError(
            "AgentRuntime is not initialized"
        )


    #
    # Create session
    #

    session = (
        container
        .session_manager
        .create_session()
    )


    session_id = session.session_id


    try:

        response = await runtime.chat(

            session_id=session_id,

            message=request.message,

            model=request.model,

            user_id="enterprise_user",

            tenant_id="default",

        )


        return {

            "session_id": session_id,

            "model": request.model,

            "response": response,

        }



    except LLMError as e:


        logger.error(
            "LLM error: %s",
            str(e),
        )


        raise HTTPException(

            status_code=503,

            detail=str(e),

        )



    except Exception as e:


        logger.exception(
            "Chat failed"
        )


        raise HTTPException(

            status_code=500,

            detail=str(e),

        )