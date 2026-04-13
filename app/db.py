import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# aici se citesc variabilele din docker compose
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "notes_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "notes_password")
DB_NAME = os.getenv("DB_NAME", "notes_db")

DATABASE_URL = (f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# engine = conexiunea cu baza de date
engine = create_engine(DATABASE_URL)

# base este clasa din care vor mosteni toate modelele
class Base(DeclarativeBase):
    pass

# factory pentru sesiuni de baza de date
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# dependency pentru FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()