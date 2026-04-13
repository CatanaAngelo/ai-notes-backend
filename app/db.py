import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Create SQLAlchemy engine using environment variables.
# This allows different configurations for dev, test, and production.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "notes_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "notes_password")
DB_NAME = os.getenv("DB_NAME", "notes_db")

DATABASE_URL = (f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Connecting to the database
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

# Sesions for the database
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Dependency used in FastAPI routes to provide a database session.
# Ensures proper opening and closing of DB connections.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()