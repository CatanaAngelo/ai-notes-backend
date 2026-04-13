from app.schemas import UserCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User
from app.schemas import UserCreate
from app.security import hash_password, verify_password

import logging

logger = logging.getLogger(__name__)

def create_user(db: Session, user_data: UserCreate) -> User:
    # Check if a user with the same email already exists.
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user is not None:
        logger.warning("Registration failed! Email already registered!", extra={"email": user_data.email})
        raise HTTPException(status_code=409, detail="Email already registered")
    
    user = User(
        email=user_data.email,
        # Hash the password before storing it in the database.
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("User registered successfully!", extra={"user_id": user.id, "email": user.email})
    return user

def login_user(db: Session, email: str, password: str) -> User:
    # Check if the user email exists.
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        logger.warning("Login failed! Check credentials!")
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    if not verify_password(password, user.hashed_password):
        logger.warning("Login failed! Password incorrect!")
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    logger.info("User logged in!", extra={"user_id": user.id, "email": user.email})
    return user