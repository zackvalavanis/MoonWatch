from decimal import Decimal
from uuid import UUID

from app.core.deps import get_current_user
from app.database import get_db
from app.models.coin import Coin
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.models.watchlist import WatchList
from app.schemas.coin import CoinOut
from app.schemas.user import (
    PositionOut,
    TransactionCreate,
    TransactionOut,
    UserCreate,
    UserResponse,
    WatchListCreate,
    WatchListOut,
)
from app.services.coinmarketcapdata import get_coin_by_id
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/main", tags=["users"])


@router.get("/watchlist", response_model=list[WatchListOut])
def get_my_watchlist(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    watchlist = db.query(WatchList).filter(WatchList.user_id == current_user.id).all()
    return watchlist


@router.post("/watchlist", response_model=WatchListOut, status_code=201)
def add_to_watchlist(
    payload: WatchListCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    coin = db.query(Coin).filter(Coin.cmc_id == payload.cmc_id).first()
    if coin is None:
        data = get_coin_by_id(cmc_id=payload.cmc_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Coin not found")

        usd = data["quote"]["USD"]
        coin = Coin(
            cmc_id=data["id"],
            name=data["name"],
            symbol=data["symbol"],
            slug=data["slug"],
            price_usd=usd["price"],
            percent_change_24h=usd["percent_change_24h"],
            market_cap=usd["market_cap"],
        )
        db.add(coin)
        db.flush()
    item = WatchList(user_id=current_user.id, coin_id=coin.id)
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Coin already in watchlist")

    db.refresh(item)
    return item


@router.delete("/watchlist/{coin_id}", status_code=200)
def delete_coin_from_watchlist(
    coin_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    coin_to_be_deleted = (
        db.query(WatchList)
        .filter(WatchList.user_id == user.id, WatchList.coin_id == coin_id)
        .first()
    )
    if coin_to_be_deleted is None:
        raise HTTPException(status_code=404, detail="Coin not found")

    db.delete(coin_to_be_deleted)
    db.commit()
    return {"message": "The coin has been removed from your watchlist"}


@router.get("/portfolio", response_model=list[PositionOut])
def get_portfolio(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):

    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()

    positions = {}

    for tx in transactions:
        p = positions.setdefault(
            tx.coin_id,
            {
                "coin": tx.coin,
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
    result = []

    for p in positions.values():
        if p["net_qty"] == 0:
            continue
        avg_cost = p["bought_cost"] / p["bought_qty"]
        current_value = p["net_qty"] * p["coin"].price_usd
        result.append(
            PositionOut(
                coin=p["coin"],
                net_quantity=p["net_qty"],
                avg_cost=avg_cost,
                current_value=current_value,
                unrealized_pnl=current_value - p["net_qty"] * avg_cost,
            )
        )
    return result


@router.post("/transaction", response_model=TransactionCreate)
def create_transaction(user: User = Depends(get_current_user), db: Session = Depends(get_db)): 
    new_transaction = 