from app.ai_client import ask_ai
from app.schemas import AskAIRequest, AskAIResponse

def generate_ai_answer(req: AskAIRequest) -> AskAIResponse:
    return ask_ai(req)