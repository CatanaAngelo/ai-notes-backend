from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import UserCreate, UserResponse, TokenResponse
from app.services import users_service
from app.security import create_access_token, get_current_user
from app.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return users_service.create_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users_service.login_user(db, form_data.username, form_data.password)
    token = create_access_token({"sub": user.email})

    return TokenResponse(
        access_token=token,
        token_type="bearer"
        )

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user