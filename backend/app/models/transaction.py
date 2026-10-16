import enum
import uuid

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class TransactionType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_tx_quantity_positive"),
        CheckConstraint("price_per_coin >= 0", name="ck_tx_price_nonneg"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    coin_id = Column(
        UUID(as_uuid=True), ForeignKey("coins.id", ondelete="CASCADE"), nullable=False
    )
    type = Column(
        Enum(
            TransactionType,
            native_enum=False,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    )
    quantity = Column(Numeric(28, 10), nullable=False)
    price_per_coin = Column(Numeric(28, 10), nullable=False)
    executed_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
