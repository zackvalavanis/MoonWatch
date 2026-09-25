import uuid

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class WatchList(Base):
    __tablename__ = "watchlist"
    __table_args__ = (UniqueConstraint("user_id", "coin_id"),)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    coin_id = Column(
        UUID(as_uuid=True), ForeignKey("coins.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
