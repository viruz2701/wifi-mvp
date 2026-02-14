from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.nas_device import nas_device as crud_nas
from app.crud.venue import venue as crud_venue
from app.crud.wireguard_peer import wireguard_peer
from app.schemas.nas_device import NASDeviceCreate, NASDeviceUpdate, NASDeviceOut
from app.schemas.wireguard_peer import WireGuardPeerCreate
from app.core.dependencies import get_current_superuser
from app.core.wireguard import add_peer

router = APIRouter()

@router.get("/", response_model=List[NASDeviceOut])
def read_nas_devices(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser),
):
    """Получить список всех NAS-устройств (только суперпользователь)"""
    devices = crud_nas.get_multi(db, skip=skip, limit=limit)
    return devices

@router.post("/", response_model=NASDeviceOut)
def create_nas_device(
    device_in: NASDeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Создать новое NAS-устройство. Если указан wireguard_pubkey, автоматически создаётся пир WireGuard."""
    # Проверяем, что площадка существует
    venue = crud_venue.get(db, id=device_in.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    # Создаём устройство (секреты будут зашифрованы в CRUD)
    device = crud_nas.create(db, obj_in=device_in)

    # Если указан публичный ключ WireGuard, создаём пир
    if device_in.wireguard_pubkey:
        # Формируем allowed_ips (например, выделяем IP из пула 192.168.99.0/24)
        # Для простоты используем фиксированную схему: 192.168.99.<id+1>/32
        # В реальном проекте нужна логика выделения свободного IP
        allowed_ips = f"192.168.99.{device.id + 1}/32"  # device.id уже сгенерирован после commit

        peer_in = WireGuardPeerCreate(
            nas_device_id=device.id,
            public_key=device_in.wireguard_pubkey,
            allowed_ips=allowed_ips,
            endpoint=f"{device.ip_address}:51820"  # стандартный порт WireGuard
        )

        # Пытаемся добавить пир в WireGuard
        try:
            add_peer(
                public_key=peer_in.public_key,
                allowed_ips=peer_in.allowed_ips,
                endpoint=peer_in.endpoint
            )
        except Exception as e:
            # Если не удалось, откатываем создание устройства
            crud_nas.remove(db, id=device.id)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to add WireGuard peer: {str(e)}"
            )

        # Сохраняем пир в базе данных
        wireguard_peer.create(db, obj_in=peer_in)

    return device

@router.get("/{id}", response_model=NASDeviceOut)
def read_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Получить NAS-устройство по ID"""
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
    """Обновить данные NAS-устройства"""
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")

    # Проверяем venue_id если он меняется
    if device_in.venue_id and device_in.venue_id != device.venue_id:
        venue = crud_venue.get(db, id=device_in.venue_id)
        if not venue:
            raise HTTPException(status_code=404, detail="New venue not found")

    # Обновляем устройство
    device = crud_nas.update(db, db_obj=device, obj_in=device_in)

    # Если изменился wireguard_pubkey, нужно обновить пир в WireGuard
    # Для простоты здесь не реализуем, но можно добавить аналогичную логику

    return device

@router.delete("/{id}", response_model=NASDeviceOut)
def delete_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser),
):
    """Удалить NAS-устройство (мягкое удаление)"""
    device = crud_nas.remove(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")

    # Если у устройства есть пир, его тоже нужно удалить из WireGuard и БД
    # Это можно сделать через событие или здесь, но для MVP оставим на усмотрение администратора
    # или реализуем позже.

    return device