from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: UUID
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
