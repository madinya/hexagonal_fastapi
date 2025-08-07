from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class CreateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_data: dict) -> User:
        normalized_email = user_data["email"].lower()
        existing_user = await self.user_repository.get_by_email(normalized_email)

        if existing_user:
            raise ValueError(f"User with email {normalized_email} already exists")

        user = User.create(**user_data)
        await self.user_repository.add(user)
        return user
