from fastapi import APIRouter, HTTPException

from app.schemas import AskAIRequest, AskAIResponse
from app.services import ai_service

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/ask-ai/", response_model=AskAIResponse)
def talk_with_openai(req: AskAIRequest) -> AskAIResponse:
    try:
        answer = ai_service.generate_ai_answer(req)
        logger.info("AI request completed successfully", extra={"model": req.model})
        return AskAIResponse(answer=answer)
    except Exception:
        logger.exception("AI is not responding", extra={"model": req.model})
        raise HTTPException(status_code=500, detail="AI service error")