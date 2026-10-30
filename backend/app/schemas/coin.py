from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CoinOut(BaseModel):
    id: UUID
    cmc_id: int
    symbol: str
    name: str
    slug: str | None
    price_usd: Decimal | None
    market_cap: Decimal | None
    percent_change_1h: float | None
    percent_change_24h: float | None
    percent_change_7d: float | None
    percent_change_30d: float | None
    percent_change_60d: float | None
    percent_change_90d: float | None
    volume: float | None
    volume_change_24h: float | None
    market_cap_dominance: float | None
    fully_diluted_market_cap: float | None
    last_updated: datetime | None

    model_config = ConfigDict(from_attributes=True)


class MarketCoinOut(BaseModel):
    cmc_id: int
    name: str
    symbol: str
    price: float
    percent_change_24h: float | None = None
    market_cap: float | None = None
