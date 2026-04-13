from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.db import get_db
from app.models import User

import os
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise RuntimeError("Missing SECRET_KEY environment variable")

# Context used by passlib to hash and verify passwords securely using bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    # Hash the plain password before storing it in the database.
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
     # Compare the plain password with the stored hashed password.
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    # Create a JWT token that includes user identity (email) in the "sub" field.
    # This token will be used to authenticate future requests.
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    logger.info("Access token created!")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Extract user information from the JWT token.
    # This ensures that only authenticated users can access protected routes.
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            logger.warning("Invalid credentials!", extra={"email": email})
            raise credentials_exception
    
    except JWTError:
        logger.warning("JWT decode failed!", extra={"email": email})
        raise credentials_exception
    
    # Find the user in the database based on the email stored in the token.
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        logger.warning("Authenticated user not found!", extra={"email": email})
        raise credentials_exception
    
    return user