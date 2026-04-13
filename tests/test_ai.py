from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

from unittest.mock import patch


def test_ask_ai_success_mocked(client):
    with patch("app.services.ai_service.ask_ai") as mock_ai:
        mock_ai.return_value = "Hello from mock"

        response = client.post(
            "/ask-ai/",
            json={
                "prompt": "hello there",
                "model": "gpt-4o-mini",
                "temperature": 0.6,
                "max_output_tokens": 160
            }
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "Hello from mock"


def test_invalid_input_pydantic_nomock(client):
    response = client.post(
        "/ask-ai/",
        json={
            "prompt": "x",
            "model": "gpt-4o-mini",
            "temperature": 0.6,
            "max_output_tokens": 160
        }
    )

    assert response.status_code == 422


def test_ai_failure_mocked(client):
    with patch("app.services.ai_service.ask_ai") as mock_ai:
        mock_ai.side_effect = Exception("boom")

        response = client.post(
            "/ask-ai/",
            json={
                "prompt": "hello there",
                "model": "gpt-4o-mini",
                "temperature": 0.6,
                "max_output_tokens": 160
            }
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "AI service error"


def test_summarize_note_success(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Summary note",
            "content": "This is a long note to summarize."
        },
        headers=auth_headers
    )
    note_id = create_response.json()["id"]

    with patch("app.services.notes_service.summarize") as mock_summary:
        mock_summary.return_value = "Short summary"

        response = client.post(f"/notes/{note_id}/summarize", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["note_id"] == note_id
    assert body["summary"] == "Short summary"
    assert body["original_length"] > 0