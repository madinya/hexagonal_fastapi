from uuid import uuid4

import pytest

from src.domain.entities.user import User
from src.infrastructure.repositories.in_memory.user_repository import \
    InMemoryUserRepository

@pytest.fixture
def user_data():
    return [
        {
            "id": "",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "age": 20,
        },
        {
            "id": "",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "age": 25,
        },
    ]


@pytest.mark.asyncio
async def test_repository_crud_operations(user_data):

    # Create and add user
    user = User.create(**user_data[0])
    repo = InMemoryUserRepository()
    repo._storage.clear()  # Ensure clean state
    await repo.add(user)

    # Test retrieval
    retrieved = await repo.get_by_id(user.id)
    assert retrieved is not None
    assert retrieved.email == user.email.lower()  

    # Test email lookup (case insensitive)

    retrieved_user_by_email = await repo.get_by_email(user.email)
    assert retrieved_user_by_email is not None
    assert retrieved_user_by_email.email == user.email.lower()

    retrieved_user_by_email_upper = await repo.get_by_email(user.email.upper())
    assert retrieved_user_by_email_upper is not None
    assert retrieved_user_by_email_upper.email == user.email.lower()

    # Test update
    user_data[0]["id"] = user.id  # Ensure ID is set for update
    user_data[0]["last_name"] = "Smith"
    updated_user = User(**user_data[0])
    await repo.update(updated_user)
    updated_user = await repo.get_by_id(user.id)
    assert updated_user is not None
    assert updated_user.first_name == user_data[0]["first_name"]
    assert updated_user.last_name == "Smith"    

    # Test list
    users = await repo.get_all()
    assert len(users) == 1
    assert users[0].last_name == "Smith"

    # Test delete
    await repo.delete(user.id)
    assert await repo.get_by_id(user.id) is None
    assert await repo.get_all() == []

