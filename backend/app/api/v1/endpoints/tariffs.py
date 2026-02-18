from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.tariff import tariff  # предполагается, что есть CRUD для тарифов
from app.schemas.tariff import TariffCreate, TariffUpdate, TariffOut
from app.crud.tariff_radius_attribute import tariff_radius_attribute
from app.schemas.tariff_radius_attribute import (
    TariffRadiusAttributeCreate,
    TariffRadiusAttributeUpdate,
    TariffRadiusAttributeOut,
    TariffRadiusAttributeNested
)
from app.core.dependencies import get_current_superuser

router = APIRouter(prefix="/tariff-plans", tags=["tariffs"])

# ---------- Базовые CRUD для тарифов (если не было) ----------
@router.get("/", response_model=List[TariffOut])
def read_tariffs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    return tariff.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=TariffOut)
def create_tariff(
    tariff_in: TariffCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    return tariff.create(db, obj_in=tariff_in)

@router.get("/{id}", response_model=TariffOut)
def read_tariff(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    obj = tariff.get(db, id=id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return obj

@router.put("/{id}", response_model=TariffOut)
def update_tariff(
    id: int,
    tariff_in: TariffUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    obj = tariff.get(db, id=id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return tariff.update(db, db_obj=obj, obj_in=tariff_in)

@router.delete("/{id}", response_model=TariffOut)
def delete_tariff(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    obj = tariff.remove(db, id=id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return obj

# ---------- Управление RADIUS-атрибутами тарифа ----------
@router.get("/{tariff_id}/radius-attributes", response_model=List[TariffRadiusAttributeNested])
def read_tariff_attributes(
    tariff_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    # Проверить существование тарифа
    t = tariff.get(db, id=tariff_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tariff not found")
    attrs = tariff_radius_attribute.get_by_tariff(db, tariff_id)
    return attrs

@router.post("/{tariff_id}/radius-attributes", response_model=TariffRadiusAttributeOut)
def add_tariff_attribute(
    tariff_id: int,
    attr_in: TariffRadiusAttributeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    if attr_in.tariff_id != tariff_id:
        raise HTTPException(status_code=400, detail="tariff_id mismatch")
    # Проверить существование тарифа и атрибута
    t = tariff.get(db, id=tariff_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tariff not found")
    from app.crud.radius_attribute import radius_attribute
    a = radius_attribute.get(db, id=attr_in.attribute_id)
    if not a:
        raise HTTPException(status_code=404, detail="Radius attribute not found")
    # Проверить, не привязан ли уже
    existing = db.query(tariff_radius_attribute.model).filter(
        tariff_radius_attribute.model.tariff_id == tariff_id,
        tariff_radius_attribute.model.attribute_id == attr_in.attribute_id,
        tariff_radius_attribute.model.deleted_at.is_(None)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Attribute already added to this tariff")
    return tariff_radius_attribute.create(db, obj_in=attr_in)

@router.put("/{tariff_id}/radius-attributes/{attr_id}", response_model=TariffRadiusAttributeOut)
def update_tariff_attribute(
    tariff_id: int,
    attr_id: int,
    attr_in: TariffRadiusAttributeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    obj = tariff_radius_attribute.get(db, id=attr_id)
    if not obj or obj.tariff_id != tariff_id:
        raise HTTPException(status_code=404, detail="Attribute not found for this tariff")
    return tariff_radius_attribute.update(db, db_obj=obj, obj_in=attr_in)

@router.delete("/{tariff_id}/radius-attributes/{attr_id}", response_model=TariffRadiusAttributeOut)
def delete_tariff_attribute(
    tariff_id: int,
    attr_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    obj = tariff_radius_attribute.get(db, id=attr_id)
    if not obj or obj.tariff_id != tariff_id:
        raise HTTPException(status_code=404, detail="Attribute not found for this tariff")
    return tariff_radius_attribute.remove(db, id=attr_id)