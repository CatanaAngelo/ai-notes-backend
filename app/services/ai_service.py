from app.ai_client import ask_ai
from app.schemas import AskAIRequest, AskAIResponse

import logging

logger = logging.getLogger(__name__)

def generate_ai_answer(req: AskAIRequest) -> AskAIResponse:
    logger.info(
        "AI request started",
        extra={
            "model": req.model,
            "prompt_length": len(req.prompt),
            "max_output_tokens": req.max_output_tokens,
            }
            )
    
    return ask_ai(req)