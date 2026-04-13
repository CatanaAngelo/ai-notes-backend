# Wrapper around OpenAI API to isolate external dependency from business logic.
from openai import OpenAI
from dotenv import load_dotenv
from .schemas import AskAIRequest
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Missing OPENAI_API_KEY")

def ask_ai(req: AskAIRequest) -> str:
    # Send prompt to OpenAI and return generated response.
    response = client.responses.create(
        input = req.prompt,
        model = req.model,
        temperature = req.temperature,
        max_output_tokens = req.max_output_tokens,
    )

    return response.output_text

def summarize(text: str) -> str:
    # Send user string to OpenAI and return summarize response.
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize this text briefly."},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content