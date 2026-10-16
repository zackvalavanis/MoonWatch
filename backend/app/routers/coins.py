from app.core.deps import get_current_user
from app.database import get_db
from app.models.coin import Coin
from app.schemas.coin import CoinOut, MarketCoinOut
from app.services.coinmarketcapdata import get_latest_listings
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import urllib.error


router = APIRouter(prefix="/coins", tags=["coins"])


@router.get("/all-coins", response_model=list[MarketCoinOut])
def get_all_coins(limit: int = Query(10, ge=1, le=100)):
    try:
        data = get_latest_listings(limit=limit)
    except urllib.error.URLError:
        raise HTTPException(status_code=502, detail="Market Data Unavailable")
    return [
        MarketCoinOut(
            cmc_id=c["id"],
            name=c["name"],
            symbol=c["symbol"],
            price=c["quote"]["USD"]["price"],
            percent_change_24h=c["quote"]["USD"]["percent_change_24h"],
            market_cap=c["quote"]["USD"]["market_cap"],
        )
        for c in data["data"]
    ]
