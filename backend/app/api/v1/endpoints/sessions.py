from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.session import session as crud_session
from app.schemas.session import SessionCreate, SessionUpdate, SessionOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[SessionOut])
def read_sessions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список всех сессий (только для суперпользователя)"""
    return crud_session.get_multi(db, skip=skip, limit=limit)

@router.get("/active", response_model=List[SessionOut])
def read_active_sessions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список активных сессий"""
    return db.query(crud_session.model).filter(
        crud_session.model.is_active == True,
        crud_session.model.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()

@router.get("/by-mac/{mac}", response_model=List[SessionOut])
def read_sessions_by_mac(
    mac: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить сессии по MAC-адресу"""
    return db.query(crud_session.model).filter(
        crud_session.model.mac_address == mac,
        crud_session.model.deleted_at.is_(None)
    ).all()

@router.get("/{id}", response_model=SessionOut)
def read_session(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить сессию по ID"""
    session = crud_session.get(db, id=id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{id}", response_model=SessionOut)
def delete_session(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить сессию (мягкое удаление)"""
    session = crud_session.remove(db, id=id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# Обратите внимание: создание и обновление сессий происходит автоматически через RADIUS,
# поэтому эндпоинты create и update не предусмотрены.