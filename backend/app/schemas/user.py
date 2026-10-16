from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.transaction import TransactionType
from app.schemas.coin import CoinOut


class WatchListOut(BaseModel):
    id: UUID
    created_at: datetime
    coin: CoinOut
    model_config = ConfigDict(from_attributes=True)


class WatchListCreate(BaseModel):
    cmc_id: int


class TransactionCreate(BaseModel):
    cmc_id: int
    type: TransactionType
    quantity: Decimal = Field(gt=0)
    price_per_coin: Decimal = Field(ge=0)
    executed_at: datetime | None = None


class TransactionOut(BaseModel):
    id: UUID
    type: TransactionType
    quantity: Decimal
    price_per_coin: Decimal
    executed_at: datetime
    coin: CoinOut
    model_config = ConfigDict(from_attributes=True)


class PositionOut(BaseModel):
    coin: CoinOut
    net_quantity: Decimal
    avg_cost: Decimal
    current_value: Decimal
    unrealized_pnl: Decimal


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
