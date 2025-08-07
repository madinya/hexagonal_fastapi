from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.domain.entities.user import User
from src.domain.use_cases.users.get_user import GetUser


@pytest.mark.asyncio
async def test_get_user_found(mock_user_repo, user_data):
    test_id = uuid4()
    mock_user = User(test_id, **user_data[0])
    repo = mock_user_repo(found_user=[mock_user])

    use_case = GetUser(repo)
    result = await use_case.execute(test_id)

    repo.get_by_id.assert_awaited_once_with(test_id)


@pytest.mark.asyncio
async def test_get_user_not_found(mock_user_repo):
    repo = mock_user_repo(found_user=[])

    use_case = GetUser(repo)
    result = await use_case.execute(uuid4())

    assert result is None
