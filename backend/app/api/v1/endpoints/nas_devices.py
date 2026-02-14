from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.nas_device import nas_device as crud_nas
from app.crud.venue import venue as crud_venue
from app.schemas.nas_device import NASDeviceCreate, NASDeviceUpdate, NASDeviceOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[NASDeviceOut])
def read_nas_devices(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    devices = crud_nas.get_multi(db, skip=skip, limit=limit)
    return devices

@router.post("/", response_model=NASDeviceOut)
def create_nas_device(
    device_in: NASDeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    # Проверяем, что площадка существует
    venue = crud_venue.get(db, id=device_in.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    device = crud_nas.create(db, obj_in=device_in)
    return device

@router.get("/{id}", response_model=NASDeviceOut)
def read_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    return device

@router.put("/{id}", response_model=NASDeviceOut)
def update_nas_device(
    id: int,
    device_in: NASDeviceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    # Проверяем venue_id если он меняется
    if device_in.venue_id and device_in.venue_id != device.venue_id:
        venue = crud_venue.get(db, id=device_in.venue_id)
        if not venue:
            raise HTTPException(status_code=404, detail="New venue not found")
    device = crud_nas.update(db, db_obj=device, obj_in=device_in)
    return device

@router.delete("/{id}", response_model=NASDeviceOut)
def delete_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    device = crud_nas.remove(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    return device