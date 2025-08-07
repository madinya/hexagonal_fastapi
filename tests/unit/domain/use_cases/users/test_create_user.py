from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from src.domain.entities.user import User
from src.domain.use_cases.users.create_user import CreateUser

@pytest.mark.asyncio
async def test_create_user_success(user_data):
    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = None
    mock_repo.add = AsyncMock()

    use_case = CreateUser(mock_repo)
    result = await use_case.execute(user_data[0])

    assert isinstance(result, User)
    assert result.first_name == user_data[0]["first_name"]
    assert result.last_name == user_data[0]["last_name"]
    assert result.email == user_data[0]["email"].strip().lower()
    assert result.age == user_data[0]["age"]
    mock_repo.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_data):
    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = User(UUID(int=0), **user_data[0])

    use_case = CreateUser(mock_repo)
    with pytest.raises(ValueError, match="already exists"):
        await use_case.execute(user_data[0])
