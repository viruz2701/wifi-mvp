from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.radius_attribute import radius_attribute
from app.schemas.radius_attribute import RadiusAttributeCreate, RadiusAttributeUpdate, RadiusAttributeOut
from app.core.dependencies import get_current_superuser

router = APIRouter(prefix="/radius-attributes", tags=["radius_attributes"])

@router.get("/", response_model=List[RadiusAttributeOut])
def read_attributes(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    return radius_attribute.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=RadiusAttributeOut)
def create_attribute(
    attr_in: RadiusAttributeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    # Проверка уникальности имени
    existing = radius_attribute.get_by_name(db, attr_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Attribute with this name already exists")
    return radius_attribute.create(db, obj_in=attr_in)

@router.get("/{id}", response_model=RadiusAttributeOut)
def read_attribute(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    attr = radius_attribute.get(db, id=id)
    if not attr:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return attr

@router.put("/{id}", response_model=RadiusAttributeOut)
def update_attribute(
    id: int,
    attr_in: RadiusAttributeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    attr = radius_attribute.get(db, id=id)
    if not attr:
        raise HTTPException(status_code=404, detail="Attribute not found")
    # Если меняется имя, проверить уникальность
    if attr_in.name and attr_in.name != attr.name:
        existing = radius_attribute.get_by_name(db, attr_in.name)
        if existing:
            raise HTTPException(status_code=400, detail="Attribute with this name already exists")
    return radius_attribute.update(db, db_obj=attr, obj_in=attr_in)

@router.delete("/{id}", response_model=RadiusAttributeOut)
def delete_attribute(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    attr = radius_attribute.remove(db, id=id)
    if not attr:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return attr