import pytest

from src.infrastructure.repositories.in_memory.user_repository import \
    InMemoryUserRepository


@pytest.fixture
async def clean_repository():
    repo = InMemoryUserRepository()
    # Clear storage between tests
    for user in await repo.get_all():
        await repo.delete(user.id)
    return repo

@pytest.fixture
def user_data():
    return [
        {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "age": 20,
        },
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "age": 25,
        },
    ]