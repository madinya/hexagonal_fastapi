from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID
    first_name: str
    last_name: str
    email: str  
    age: Optional[int] = None

    @classmethod
    def create(cls, **kwargs):
        return cls(
            id=uuid4(),
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"],
            email=kwargs["email"],
            age=kwargs.get("age"),
        )
