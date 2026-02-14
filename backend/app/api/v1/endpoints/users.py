from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate, UserOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def read_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    # Проверяем, не занят ли email
    existing = crud_user.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud_user.create(db, obj_in=user_in)
    return user