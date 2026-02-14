from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.venue import venue as crud_venue
from app.schemas.venue import VenueCreate, VenueUpdate, VenueOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[VenueOut])
def read_venues(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    venues = crud_venue.get_multi(db, skip=skip, limit=limit)
    return venues

@router.post("/", response_model=VenueOut)
def create_venue(
    venue_in: VenueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    venue = crud_venue.create(db, obj_in=venue_in)
    return venue

@router.get("/{id}", response_model=VenueOut)
def read_venue(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
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
    current_user = Depends(get_current_superuser),
):
    venue = crud_venue.get(db, id=id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    venue = crud_venue.update(db, db_obj=venue, obj_in=venue_in)
    return venue

@router.delete("/{id}", response_model=VenueOut)
def delete_venue(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    venue = crud_venue.remove(db, id=id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue