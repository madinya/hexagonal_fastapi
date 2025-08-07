from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    _instance = None
    _storage: Dict[UUID, User] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryUserRepository, cls).__new__(cls)
        return cls._instance

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self._storage.get(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        normalized_email = email.lower()
        return next(
            (
                user
                for user in self._storage.values()
                if user.email.lower() == normalized_email
            ),
            None,
        )

    async def get_all(self) -> List[User]:
        return list(self._storage.values())

    async def add(self, user: User) -> None:
        self._storage[user.id] = user

    async def update(self, user: User) -> None:
        self._storage[user.id] = user

    async def delete(self, user_id: UUID) -> None:
        self._storage.pop(user_id, None)
