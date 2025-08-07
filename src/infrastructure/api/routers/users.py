from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.domain.use_cases.users.create_user import CreateUser
from src.domain.use_cases.users.get_user import GetUser
from src.domain.use_cases.users.list_users import ListUsers
from src.infrastructure.api.schemas.user import UserCreateInput, UserResponse
from src.infrastructure.repositories.in_memory.user_repository import \
    InMemoryUserRepository

router = APIRouter(prefix="/users", tags=["users"])

_repository = InMemoryUserRepository()


def get_repository():
    return _repository


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreateInput,
    repository: InMemoryUserRepository = Depends(get_repository),
):
    try:
        use_case = CreateUser(repository)
        user = await use_case.execute(user_data.dict())
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID, repository: InMemoryUserRepository = Depends(get_repository)
):
    use_case = GetUser(repository)
    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserResponse])
async def list_users(repository: InMemoryUserRepository = Depends(get_repository)):
    use_case = ListUsers(repository)
    return await use_case.execute()
