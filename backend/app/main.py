from fastapi import FastAPI  # noqa: I001
from app.database import Base, engine
from app.services.coinmarketcapdata import get_latest_listings
from app.models import coin, user, watchlist, transaction  # noqa: F401
from app.routers.auth import router as auth_router
from app.routers.users import router as user_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
async def get_health():
    return {"Status": "Ok"}


@app.get("/prices")
def get_prices(limit: int = 10):
    return get_latest_listings(limit=limit)
