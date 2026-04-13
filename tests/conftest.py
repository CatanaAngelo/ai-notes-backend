import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import get_db
from app.models import Base

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")
os.environ.setdefault("DB_NAME", "test_db")

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_token(client):
    register_response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "secret123"
        }
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "secret123"
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return token


@pytest.fixture
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}