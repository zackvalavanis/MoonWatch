from fastapi import FastAPI  # noqa: I001
from app.database import Base

app = FastAPI()

Base.metadata.create_all()


@app.get("/health")
async def get_health():
    return {"Status": "Ok"}
