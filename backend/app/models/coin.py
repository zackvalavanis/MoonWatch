import uuid

from sqlalchemy import Column, DateTime, Float, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Coin(Base):
    __tablename__ = "coins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cmc_id = Column(Integer, nullable=False, index=True, unique=True)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String)
    price_usd = Column(Numeric(28, 10))
    percent_change_24h = Column(Float)
    market_cap = Column(Numeric(28, 2))
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
