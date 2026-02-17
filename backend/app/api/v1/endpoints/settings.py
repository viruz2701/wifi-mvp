from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.setting import setting as crud_setting
from app.schemas.setting import SettingCreate, SettingUpdate, SettingOut
from app.core.dependencies import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[SettingOut])
def read_settings(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список всех настроек."""
    return crud_setting.get_multi(db, skip=skip, limit=limit)

@router.get("/{key}", response_model=SettingOut)
def read_setting(
    key: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить настройку по ключу."""
    setting = crud_setting.get_by_key(db, key=key)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@router.put("/{key}", response_model=SettingOut)
def update_setting(
    key: str,
    setting_in: SettingUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Обновить настройку."""
    setting = crud_setting.get_by_key(db, key=key)
    if not setting:
        # Если не существует, можно создать
        setting = crud_setting.create(db, obj_in=SettingCreate(key=key, **setting_in.dict()))
        return setting
    return crud_setting.update(db, db_obj=setting, obj_in=setting_in)

@router.delete("/{key}", response_model=SettingOut)
def delete_setting(
    key: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить настройку."""
    setting = crud_setting.get_by_key(db, key=key)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return crud_setting.remove(db, id=setting.id)