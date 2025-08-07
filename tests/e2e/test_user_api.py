import uuid

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.api.schemas.user import UserCreateInput
from src.main import app

client = TestClient(app)

@pytest.fixture
def user_create_input(user_data):
    return UserCreateInput(**user_data[0])  # Convert first user to Pydantic model


def test_full_user_lifecycle(user_create_input):
    create_response = client.post(
        "/users/",   json=user_create_input.dict() 
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Test duplicate prevention
    duplicate_response = client.post(
        "/users/", json= user_create_input.dict().copy() | {"email": user_create_input.email.upper()}  
    )
    assert duplicate_response.status_code == 400

    # Test get user
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == user_create_input.email.lower()
