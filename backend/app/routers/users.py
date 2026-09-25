from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/main", tags=["users"])


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users
