from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# model pydantic pentru request body
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=5)

# model pydantic pentru raspuns
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# model pydantic pentru ask-ai request
class AskAIRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=200)
    model: str = Field(default="gpt-4o-mini")
    max_output_tokens: int = Field(default=150, ge=1, le=200)
    temperature: float = Field(default=0.8, ge=0.0, le=2)

#model pydantic pentru ask-ai raspuns
class AskAIResponse(BaseModel):
    answer: str

class UserCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6, max_length=64)

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class NoteSummaryResponse(BaseModel):
    note_id: int
    summary: str
    original_length: int