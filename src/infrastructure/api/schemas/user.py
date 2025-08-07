from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateInput(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, gt=0, lt=120)


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    age: Optional[int]

    class Config:
        from_attributes = True
