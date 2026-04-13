from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_note_success(client, auth_headers):
    response = client.post(
        "/notes/",
        json={
            "title": "Test title",
            "content": "Test content here"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Test title"
    assert body["content"] == "Test content here"
    assert "id" in body
    assert "created_at" in body

def test_create_note_requires_auth(client):
    response = client.post(
        "/notes/",
        json={
            "title": "Test title",
            "content": "Test content here"
        }
    )

    assert response.status_code == 401

def test_invalid_input_422(client, auth_headers):
    response = client.post(
        "/notes/",
        json={
            "title": "aa",
            "content": "bb"
        },
        headers=auth_headers
    )

    assert response.status_code == 422

def test_get_existing_note(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Test title",
            "content": "Test content here"
        },
        headers=auth_headers
    )
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == note_id

def test_update_existing_note(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Old title",
            "content": "Old content here"
        },
        headers=auth_headers
    )
    note_id = create_response.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        json={
            "title": "New title",
            "content": "New content here"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["content"] == "New content here"

def test_delete_existing_note(client, auth_headers):
    create_response = client.post(
        "/notes/",
        json={
            "title": "Delete me",
            "content": "Delete content here"
        },
        headers=auth_headers
    )
    note_id = create_response.json()["id"]

    delete_response = client.delete(f"/notes/{note_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_get_only_own_notes(client, auth_headers):
    client.post(
        "/notes/",
        json={
            "title": "My note",
            "content": "My content here"
        },
        headers=auth_headers
    )

    client.post("/register", json={"email": "other@example.com", "password": "secret123"})
    login_other = client.post(
        "/login",
        data={"username": "other@example.com", "password": "secret123"}
    )
    other_token = login_other.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    client.post(
        "/notes/",
        json={
            "title": "Other note",
            "content": "Other content here"
        },
        headers=other_headers
    )

    response = client.get("/notes/", headers=auth_headers)

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 1
    assert notes[0]["title"] == "My note"