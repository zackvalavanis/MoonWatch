from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CoinOut(BaseModel):
    id: UUID
    cmc_id: int
    symbol: str
    name: str
    slug: str | None = None
    price_usd: float | None = None
    percent_change_24h: float | None = None
    market_cap: float | None = None
    last_updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class MarketCoinOut(BaseModel):
    cmc_id: int
    name: str
    symbol: str
    price: float
    percent_change_24h: float | None = None
    market_cap: float | None = None
