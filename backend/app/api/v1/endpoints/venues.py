from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.crud.venue import venue as crud_venue
from app.schemas.venue import VenueCreate, VenueUpdate, VenueOut
from app.core.dependencies import get_current_superuser, get_current_active_user
from app.models.venue import Venue
from app.models.user import User

router = APIRouter()

# Эндпоинт для списка площадок (без слеша)
@router.get("", response_model=List[VenueOut])
def read_venues(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
):
    """Получить список всех площадок (доступно любому аутентифицированному пользователю)"""
    return crud_venue.get_multi(db, skip=skip, limit=limit)

# Эндпоинт для списка площадок (со слешем) – чтобы избежать редиректа
@router.get("/", response_model=List[VenueOut])
def read_venues_with_slash(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
):
    """Получить список всех площадок (доступно любому аутентифицированному пользователю)"""
    return crud_venue.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=VenueOut)
def create_venue(
    venue_in: VenueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать новую площадку (только суперпользователь)"""
    if venue_in.domain:
        existing = db.query(Venue).filter(
            and_(
                Venue.domain == venue_in.domain,
                Venue.deleted_at.is_(None)
            )
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Domain already in use")
    return crud_venue.create(db, obj_in=venue_in)

@router.get("/{id}", response_model=VenueOut)
def read_venue(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    venue = crud_venue.get(db, id=id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.put("/{id}", response_model=VenueOut)
def update_venue(
    id: int,
    venue_in: VenueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    venue = crud_venue.get(db, id=id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    if venue_in.domain is not None and venue_in.domain != venue.domain:
        existing = db.query(Venue).filter(
            and_(
                Venue.domain == venue_in.domain,
                Venue.deleted_at.is_(None)
            )
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Domain already in use")
    return crud_venue.update(db, db_obj=venue, obj_in=venue_in)

@router.delete("/{id}", response_model=VenueOut)
def delete_venue(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    venue = crud_venue.remove(db, id=id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue