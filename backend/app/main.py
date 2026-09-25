from fastapi import FastAPI  # noqa: I001
from app.database import Base, engine
from app.services.coinmarketcapdata import get_latest_listings

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health")
async def get_health():
    return {"Status": "Ok"}


@app.get("/prices")
async def get_prices(limit: int = 10):
    return get_latest_listings(limit=limit)
