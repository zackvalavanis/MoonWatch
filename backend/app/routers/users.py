import urllib.error
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from app.core.deps import get_current_user
from app.database import get_db
from app.models.coin import Coin
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.models.watchlist import WatchList
from app.schemas.user import (
    PositionOut,
    TransactionCreate,
    TransactionOut,
    WatchListCreate,
    WatchListOut,
)
from app.services.coinmarketcapdata import get_coin_by_id
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix="/main", tags=["users"])

STALE_AFTER = timedelta(seconds=60)


# ---------- coin helpers ----------


def _dec(value):
    """CMC returns floats; convert to Decimal for Numeric columns."""
    return None if value is None else Decimal(str(value))


def _apply_cmc_data(coin: Coin, data: dict) -> None:
    usd = data["quote"]["USD"]
    coin.cmc_id = data["id"]
    coin.name = data["name"]
    coin.symbol = data["symbol"]
    coin.slug = data.get("slug")
    coin.price_usd = _dec(usd.get("price"))
    coin.market_cap = _dec(usd.get("market_cap"))
    coin.percent_change_1h = usd.get("percent_change_1h")
    coin.percent_change_24h = usd.get("percent_change_24h")
    coin.percent_change_7d = usd.get("percent_change_7d")
    coin.percent_change_30d = usd.get("percent_change_30d")
    coin.percent_change_60d = usd.get("percent_change_60d")
    coin.percent_change_90d = usd.get("percent_change_90d")
    coin.volume = usd.get("volume_24h")
    coin.volume_change_24h = usd.get("volume_change_24h")
    coin.market_cap_dominance = usd.get("market_cap_dominance")
    coin.fully_diluted_market_cap = usd.get("fully_diluted_market_cap")
    coin.last_updated = datetime.now(timezone.utc)  # when WE last fetched it


def get_or_refresh_coin(db: Session, cmc_id: int) -> Coin:
    """Return a fresh Coin, creating it or refetching from CMC if stale."""
    coin = db.query(Coin).filter(Coin.cmc_id == cmc_id).first()

    if (
        coin
        and coin.last_updated
        and datetime.now(timezone.utc) - coin.last_updated < STALE_AFTER
    ):
        return coin

    try:
        data = get_coin_by_id(cmc_id=cmc_id)
    except urllib.error.URLError:
        if coin:
            return coin  # CMC down or rate-limited: serve stale data
        raise HTTPException(status_code=502, detail="Price service unavailable")

    if data is None:
        if coin:
            return coin
        raise HTTPException(status_code=404, detail="Coin not found")

    if coin is None:
        coin = Coin()
        db.add(coin)
    _apply_cmc_data(coin, data)
    db.flush()
    return coin


# ---------- watchlist ----------


@router.get("/watchlist", response_model=list[WatchListOut])
def get_my_watchlist(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    items = (
        db.query(WatchList)
        .options(joinedload(WatchList.coin))
        .filter(WatchList.user_id == current_user.id)
        .all()
    )
    for item in items:
        get_or_refresh_coin(db, item.coin.cmc_id)
    db.commit()

    return (
        db.query(WatchList)
        .options(joinedload(WatchList.coin))
        .filter(WatchList.user_id == current_user.id)
        .all()
    )


@router.delete("/watchlist/{coin_id}", status_code=200)
def delete_coin_from_watchlist(
    coin_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(WatchList)
        .filter(WatchList.user_id == user.id, WatchList.coin_id == coin_id)
        .first()
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    db.delete(item)
    db.commit()
    return {"message": "The coin has been removed from your watchlist"}


# ---------- portfolio ----------


@router.get("/portfolio", response_model=list[PositionOut])
def get_portfolio(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    transactions = (
        db.query(Transaction)
        .options(joinedload(Transaction.coin))
        .filter(Transaction.user_id == user.id)
        .all()
    )

    positions = {}
    for tx in transactions:
        p = positions.setdefault(
            tx.coin_id,
            {
                "cmc_id": tx.coin.cmc_id,
                "net_qty": Decimal(0),
                "bought_qty": Decimal(0),
                "bought_cost": Decimal(0),
            },
        )
        if tx.type == TransactionType.BUY:
            p["net_qty"] += tx.quantity
            p["bought_qty"] += tx.quantity
            p["bought_cost"] += tx.quantity * tx.price_per_coin
        else:
            p["net_qty"] -= tx.quantity

    # Refresh prices for coins still held, then save them
    for p in positions.values():
        if p["net_qty"] > 0:
            p["coin"] = get_or_refresh_coin(db, p["cmc_id"])
    db.commit()

    result = []
    for p in positions.values():
        if p["net_qty"] <= 0 or p["bought_qty"] == 0:
            continue
        coin = p["coin"]
        avg_cost = p["bought_cost"] / p["bought_qty"]
        if coin.price_usd is None:
            continue
        current_value = p["net_qty"] * coin.price_usd
        result.append(
            PositionOut(
                coin=coin,
                net_quantity=p["net_qty"],
                avg_cost=avg_cost,
                current_value=current_value,
                unrealized_pnl=current_value - p["net_qty"] * avg_cost,
            )
        )
    return result


# ---------- transactions ----------


@router.post("/transaction", response_model=TransactionOut, status_code=201)
def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    coin = get_or_refresh_coin(db, transaction_data.cmc_id)

    new_transaction = Transaction(
        user_id=current_user.id,
        coin_id=coin.id,
        type=transaction_data.type.value,
        quantity=transaction_data.quantity,
        price_per_coin=transaction_data.price_per_coin,
        executed_at=transaction_data.executed_at or datetime.now(timezone.utc),
    )
    db.add(new_transaction)
    db.commit()

    return (
        db.query(Transaction)
        .options(joinedload(Transaction.coin))
        .filter(Transaction.id == new_transaction.id)
        .first()
    )
