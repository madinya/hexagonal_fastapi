import pytest

from unittest.mock import AsyncMock, MagicMock
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


@pytest.fixture
def mock_user_repo():
    def _mock_repo(
        existing_users=None, 
        found_user=None,
        raise_error=None
    ):
        repo = AsyncMock()
        
        repo.get_all.return_value = existing_users or []
        
        if found_user:
            repo.get_by_id.return_value = found_user
            repo.get_by_email.return_value = found_user
        else:
            repo.get_by_id.return_value = None
            repo.get_by_email.return_value = None
            
        if raise_error:
            repo.add.side_effect = raise_error
            repo.update.side_effect = raise_error
        else:
            repo.add.side_effect = lambda user: user
            repo.update.side_effect = lambda user: user
            
        return repo
    
    return _mock_repo