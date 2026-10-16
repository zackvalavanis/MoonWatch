from app.core.deps import get_current_user
from app.database import get_db
from app.models.coin import Coin
from app.models.user import User
from app.models.watchlist import WatchList
from app.schemas.coin import CoinOut
from app.schemas.user import UserCreate, UserResponse, WatchListCreate, WatchListOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.services.coinmarketcapdata import get_coin_by_id

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
