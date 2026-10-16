from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.coin import CoinOut


class WatchListOut(BaseModel):
    id: UUID
    created_at: datetime
    coin: CoinOut
    model_config = ConfigDict(from_attributes=True)


class WatchListCreate(BaseModel):
    cmc_id: int


class UserResponse(BaseModel):
    id: UUID
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    created_at: datetime
    watchlist: list[WatchListOut] = []

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
