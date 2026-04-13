# AI Notes Backend

A production-style FastAPI backend for authenticated note management, featuring PostgreSQL persistence, JWT-based access control, and OpenAI-powered summarization.

---

## Features

* User registration and login
* JWT authentication
* Protected routes with user context
* Notes CRUD per authenticated user
* Ownership validation (users only access their own notes)
* Pagination and search functionality
* OpenAI integration for note summarization
* Dockerized PostgreSQL setup
* Alembic database migrations
* Automated tests with pytest

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy 2.0
* PostgreSQL
* Alembic
* Docker / Docker Compose
* Passlib + bcrypt
* Python-Jose (JWT)
* OpenAI API
* Pytest

---

## Project Structure

```
app/
├── main.py
├── db.py
├── models.py
├── schemas.py
├── security.py
├── ai_client.py
├── routers/
│   ├── auth.py
│   ├── notes.py
│   └── ai.py
└── services/
    ├── users_service.py
    ├── notes_service.py
    └── ai_service.py

tests/
├── conftest.py
├── test_notes.py
└── test_ai.py
```

---

## Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd practice1
```

---

### 2. Create a `.env` file

```
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

DB_HOST=db
DB_PORT=5432
DB_USER=notes_user
DB_PASSWORD=notes_password
DB_NAME=notes_db
```

---

### 3. Start the project

```
docker compose up --build
```

---

### 4. Run migrations

```
docker compose exec api alembic upgrade head
```

---

## API Endpoints

### Auth

* `POST /register`
* `POST /login`
* `GET /me`

### Notes

* `GET /notes/`
* `POST /notes/`
* `GET /notes/{note_id}`
* `PUT /notes/{note_id}`
* `DELETE /notes/{note_id}`
* `POST /notes/{note_id}/summarize`

### AI

* `POST /ask-ai/`

---

## Example Flow

1. Register a user
2. Login to receive JWT token
3. Authorize in Swagger using the token
4. Create notes
5. Retrieve only your own notes
6. Search notes
7. Summarize notes using AI

---

## Testing

Run tests with:

```
pytest
```

Tests include:

* authentication flow
* notes CRUD
* ownership validation
* AI summarization (mocked)

---

## What I Implemented

This project was built to practice backend engineering fundamentals and AI integration.

Key areas:

* layered FastAPI architecture (routers → services → models)
* authentication and authorization using JWT
* relational database design (User → Notes)
* database migrations with Alembic
* secure per-user data access
* OpenAI integration in backend services
* testable architecture with dependency overrides
* automated testing with pytest

---

## Future Improvements

* centralized config management
* background tasks (emails, async jobs)
* rate limiting for AI endpoints
* refresh tokens
* caching layer (Redis)
* CI/CD pipeline

---

## Notes

This project is focused on learning core backend concepts and building a solid foundation for real-world backend and AI-integrated systems.
