from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.domain.entities.user import User
from src.domain.use_cases.users.get_user import GetUser


@pytest.mark.asyncio
async def test_get_user_found():
    test_id = uuid4()
    mock_user = User(test_id, "John", "Doe", "john@example.com")
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = mock_user

    use_case = GetUser(mock_repo)
    result = await use_case.execute(test_id)

    assert result == mock_user
    mock_repo.get_by_id.assert_awaited_once_with(test_id)


@pytest.mark.asyncio
async def test_get_user_not_found():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None

    use_case = GetUser(mock_repo)
    result = await use_case.execute(uuid4())

    assert result is None
