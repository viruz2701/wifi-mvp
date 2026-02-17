from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.sms_provider import sms_provider as crud_provider
from app.schemas.sms_provider import SMSProviderCreate, SMSProviderUpdate, SMSProviderOut
from app.core.dependencies import get_current_superuser
from app.models.sms_provider import SMSProviderType

router = APIRouter()

@router.get("/types", response_model=List[str])
def get_provider_types(
    current_user = Depends(get_current_superuser),
):
    """
    Возвращает список доступных типов SMS-провайдеров.
    Используется на фронтенде для динамического построения формы.
    """
    return [t.value for t in SMSProviderType]

@router.get("", response_model=List[SMSProviderOut])
def read_providers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список всех SMS-провайдеров."""
    return crud_provider.get_multi(db, skip=skip, limit=limit)

@router.post("", response_model=SMSProviderOut)
def create_provider(
    provider_in: SMSProviderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Создать нового SMS-провайдера."""
    return crud_provider.create(db, obj_in=provider_in)

@router.get("/{id}", response_model=SMSProviderOut)
def read_provider(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить провайдера по ID."""
    provider = crud_provider.get(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="SMS provider not found")
    return provider

@router.put("/{id}", response_model=SMSProviderOut)
def update_provider(
    id: int,
    provider_in: SMSProviderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Обновить данные провайдера."""
    provider = crud_provider.get(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="SMS provider not found")
    return crud_provider.update(db, db_obj=provider, obj_in=provider_in)

@router.delete("/{id}", response_model=SMSProviderOut)
def delete_provider(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить провайдера (мягкое удаление)."""
    provider = crud_provider.remove(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="SMS provider not found")
    return provider

@router.post("/{id}/set-active", response_model=SMSProviderOut)
def set_active_provider(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """
    Установить данного провайдера как активного.
    Автоматически сбрасывает флаг is_active у всех остальных провайдеров.
    """
    # Сначала сбрасываем is_active у всех
    db.query(crud_provider.model).update({"is_active": False})
    # Затем активируем нужного
    provider = crud_provider.get(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="SMS provider not found")
    provider.is_active = True
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider