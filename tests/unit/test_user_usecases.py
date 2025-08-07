from uuid import UUID

import pytest

from src.domain.entities.user import User
from src.domain.use_cases.users.create_user import CreateUser
from src.domain.use_cases.users.get_user import GetUser
from src.domain.use_cases.users.list_users import ListUsers
from src.infrastructure.repositories.in_memory.user_repository import \
    InMemoryUserRepository


@pytest.fixture
def repository():
    repo = InMemoryUserRepository()
    repo._storage.clear()
    return repo


@pytest.mark.asyncio
async def test_create_user_success(repository, user_data):
    use_case = CreateUser(repository)
    user = await use_case.execute(user_data[0])

    assert isinstance(user, User)
    assert await repository.get_by_id(user.id) == user


@pytest.mark.asyncio
async def test_create_user_duplicate_email(repository, user_data):
    use_case = CreateUser(repository)
    await use_case.execute(user_data[0])

    with pytest.raises(ValueError, match="already exists"):
        await use_case.execute(user_data[0])


@pytest.mark.asyncio
async def test_get_user_found(repository, user_data):
    user = User.create(**user_data[0])
    await repository.add(user)

    use_case = GetUser(repository)
    retrieved_user = await use_case.execute(user.id)

    assert retrieved_user == user


@pytest.mark.asyncio
async def test_get_user_not_found(repository):
    use_case = GetUser(repository)
    non_existent_id = UUID("00000000-0000-0000-0000-000000000000")
    user = await use_case.execute(non_existent_id)

    assert user is None


@pytest.mark.asyncio
async def test_list_users(repository, user_data):
    user1 = User.create(**user_data[0])
    user2 = User.create(**user_data[1])
    await repository.add(user1)
    await repository.add(user2)

    use_case = ListUsers(repository)
    users = await use_case.execute()

    assert len(users) == 2
    assert user1 in users
    assert user2 in users
