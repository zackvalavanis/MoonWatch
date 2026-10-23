from fastapi import FastAPI  # noqa: I001
from app.database import Base, engine
from app.services.coinmarketcapdata import get_latest_listings
from app.models import coin, user, watchlist, transaction  # noqa: F401
from app.routers.auth import router as auth_router
from app.routers.users import router as user_router
from app.routers.coins import router as coins_router
from app.config import CORS_ORIGINS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(coins_router)


@app.get("/health")
async def get_health():
    return {"Status": "Ok"}


@app.get("/prices")
def get_prices(limit: int = 10):
    return get_latest_listings(limit=limit)
