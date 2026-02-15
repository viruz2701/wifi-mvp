from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate, UserOut
from app.core.dependencies import get_current_superuser, get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[UserOut])
def read_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_superuser),
):
    """Получить список всех администраторов (только суперпользователь)"""
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/", response_model=List[UserOut])
def read_users_with_slash(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_superuser),
):
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    existing = crud_user.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.post("", response_model=UserOut)
def create_user_without_slash(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать нового пользователя (без слеша в URL)"""
    return create_user(user_in, db, current_user)

@router.get("/me", response_model=UserOut)
def read_current_user(
    current_user: User = Depends(get_current_active_user),
):
    return current_user

@router.get("/{id}", response_model=UserOut)
def read_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    user = crud_user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}", response_model=UserOut)
def update_user(
    id: int,
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    user = crud_user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Не обновляем пароль в этом примере; при необходимости можно добавить логику
    for key, value in user_in.dict(exclude_unset=True).items():
        if key != "password":
            setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}", response_model=UserOut)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    user = crud_user.remove(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
