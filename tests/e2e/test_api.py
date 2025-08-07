import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_full_user_flow():
    import uuid

    test_email = f"user_{uuid.uuid4().hex[:8]}@example.com"

    # Test creation
    create_response = client.post(
        "/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": test_email,
            "age": 30,
        },
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Test duplicate prevention with different case
    duplicate_response = client.post(
        "/users/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": test_email.upper(),  # Different case
            "age": 30,
        },
    )
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"]

    # Verify the original user exists
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == test_email.lower()
