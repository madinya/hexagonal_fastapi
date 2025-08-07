import pytest

from src.domain.entities.user import User
from src.domain.use_cases.users.create_user import CreateUser

@pytest.mark.asyncio
async def test_create_user_success(user_data, mock_user_repo):
    repo = mock_user_repo()

    use_case = CreateUser(repo)
    result = await use_case.execute(user_data[0])

    repo.add.assert_awaited_once()
    assert isinstance(result, User)
    assert result.first_name == user_data[0]["first_name"]
    assert result.last_name == user_data[0]["last_name"]
    assert result.email == user_data[0]["email"].strip().lower()
    assert result.age == user_data[0]["age"]



@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_data, mock_user_repo):
    repo = mock_user_repo(found_user=user_data)

    use_case = CreateUser(repo)
    with pytest.raises(ValueError, match="already exists"):
        await use_case.execute(user_data[0])
