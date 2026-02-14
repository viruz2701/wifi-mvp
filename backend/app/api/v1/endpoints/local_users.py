from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.local_user import local_user as crud_local_user
from app.schemas.local_user import LocalUserCreate, LocalUserUpdate, LocalUserOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[LocalUserOut])
def read_local_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список всех локальных пользователей"""
    return crud_local_user.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=LocalUserOut)
def create_local_user(
    user_in: LocalUserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Создать нового локального пользователя (пароль хэшируется автоматически)"""
    # Проверяем уникальность username в рамках площадки
    existing = crud_local_user.get_by_username(db, username=user_in.username, venue_id=user_in.venue_id)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists for this venue")
    return crud_local_user.create(db, obj_in=user_in)

@router.get("/{id}", response_model=LocalUserOut)
def read_local_user(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить локального пользователя по ID"""
    user = crud_local_user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Local user not found")
    return user

@router.put("/{id}", response_model=LocalUserOut)
def update_local_user(
    id: int,
    user_in: LocalUserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Обновить данные локального пользователя (можно сменить пароль)"""
    user = crud_local_user.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Local user not found")
    # Если меняется username, проверяем уникальность
    if user_in.username and user_in.username != user.username:
        existing = crud_local_user.get_by_username(db, username=user_in.username, venue_id=user.venue_id)
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists for this venue")
    return crud_local_user.update(db, db_obj=user, obj_in=user_in)

@router.delete("/{id}", response_model=LocalUserOut)
def delete_local_user(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить локального пользователя (мягкое удаление)"""
    user = crud_local_user.remove(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Local user not found")
    return user