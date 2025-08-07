from typing import Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class GetUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)
