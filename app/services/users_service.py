from app.schemas import UserCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User
from app.schemas import UserCreate
from app.security import hash_password, verify_password

def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    return user