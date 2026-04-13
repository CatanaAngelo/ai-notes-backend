from app.ai_client import ask_ai
from app.schemas import AskAIRequest

def generate_ai_answer(req: AskAIRequest) -> str:
    return ask_ai(req)