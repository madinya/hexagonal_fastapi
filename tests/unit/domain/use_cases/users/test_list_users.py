from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.domain.entities.user import User
from src.domain.use_cases.users.list_users import ListUsers


@pytest.mark.asyncio
async def test_list_users():
    mock_users = [
        User(uuid4(), "John", "Doe", "john@example.com"),
        User(uuid4(), "Jane", "Smith", "jane@example.com"),
    ]
    mock_repo = AsyncMock()
    mock_repo.get_all.return_value = mock_users

    use_case = ListUsers(mock_repo)
    result = await use_case.execute()

    assert len(result) == 2
    assert all(isinstance(u, User) for u in result)
    mock_repo.get_all.assert_awaited_once()
