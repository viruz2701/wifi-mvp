from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.crm_provider import crm_provider
from app.schemas.crm_provider import CRMProviderCreate, CRMProviderUpdate, CRMProviderOut
from app.core.dependencies import get_current_superuser
from app.models.crm_provider import CRMProviderType
from app.tasks.crm import bulk_export_to_crm

router = APIRouter(prefix="/crm", tags=["crm"])

@router.get("/types", response_model=List[str])
def get_provider_types(
    current_user = Depends(get_current_superuser),
):
    """Возвращает список доступных типов CRM-провайдеров."""
    return [t.value for t in CRMProviderType]

@router.get("/providers", response_model=List[CRMProviderOut])
def read_providers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список всех CRM-провайдеров."""
    return crm_provider.get_multi(db, skip=skip, limit=limit)

@router.post("/providers", response_model=CRMProviderOut)
def create_provider(
    provider_in: CRMProviderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Создать нового CRM-провайдера."""
    return crm_provider.create(db, obj_in=provider_in)

@router.get("/providers/{id}", response_model=CRMProviderOut)
def read_provider(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить провайдера по ID."""
    provider = crm_provider.get(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="CRM provider not found")
    return provider

@router.put("/providers/{id}", response_model=CRMProviderOut)
def update_provider(
    id: int,
    provider_in: CRMProviderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Обновить данные провайдера."""
    provider = crm_provider.get(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="CRM provider not found")
    return crm_provider.update(db, db_obj=provider, obj_in=provider_in)

@router.delete("/providers/{id}", response_model=CRMProviderOut)
def delete_provider(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить провайдера."""
    provider = crm_provider.remove(db, id=id)
    if not provider:
        raise HTTPException(status_code=404, detail="CRM provider not found")
    return provider

@router.post("/export-now")
async def export_now(
    background_tasks: BackgroundTasks,
    venue_id: Optional[int] = Query(None, description="ID площадки (необязательно)"),
    from_date: Optional[str] = Query(None, description="Начало периода (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Конец периода (YYYY-MM-DD)"),
    current_user = Depends(get_current_superuser)
):
    """Запускает фоновую задачу отправки всех непереданных контактов в CRM."""
    background_tasks.add_task(bulk_export_to_crm, venue_id, from_date, to_date)
    return {"message": "Export task started"}