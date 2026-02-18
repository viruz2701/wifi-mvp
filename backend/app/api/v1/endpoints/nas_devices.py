from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.crud.nas_device import nas_device as crud_nas
from app.crud.venue import venue as crud_venue
from app.crud.wireguard_peer import wireguard_peer
from app.schemas.nas_device import NASDeviceCreate, NASDeviceUpdate, NASDeviceOut
from app.schemas.wireguard_peer import WireGuardPeerCreate
from app.core.dependencies import get_current_superuser, get_current_active_user
from app.core.security import encrypt_secret, decrypt_secret
from app.core.wireguard import add_peer, generate_keypair
from app.models.user import User
from app.models.nas_device import NASDevice
from app.models.venue import Venue
from app.nas import get_nas_instance
import subprocess

router = APIRouter()

# Эндпоинты для управления (перезагрузка, сброс сессий)
@router.post("/{id}/reboot")
def reboot_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    nas = get_nas_instance(device)
    if not nas:
        raise HTTPException(status_code=400, detail="Unsupported device type")
    try:
        nas.reboot()
        return {"message": "Reboot command sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reboot: {e}")

@router.post("/{id}/disconnect-all")
def disconnect_all_sessions(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    nas = get_nas_instance(device)
    if not nas:
        raise HTTPException(status_code=400, detail="Unsupported device type")
    try:
        nas.disconnect_all_sessions()
        return {"message": "Disconnect all command sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to disconnect: {e}")

# Получение списка (без слеша)
@router.get("", response_model=List[NASDeviceOut])
def read_nas_devices(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
):
    devices = crud_nas.get_multi(db, skip=skip, limit=limit)
    return devices

# Получение списка (со слешем)
@router.get("/", response_model=List[NASDeviceOut])
def read_nas_devices_with_slash(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
):
    devices = crud_nas.get_multi(db, skip=skip, limit=limit)
    return devices

# Создание (со слешем)
@router.post("/", response_model=NASDeviceOut)
def create_nas_device(
    device_in: NASDeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать новое NAS-устройство (только суперпользователь)"""
    # Проверка уникальности IP
    existing = db.query(NASDevice).filter(
        NASDevice.ip_address == device_in.ip_address,
        NASDevice.deleted_at.is_(None)
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Устройство с IP-адресом {device_in.ip_address} уже существует."
        )

    # Проверка существования площадки
    venue = crud_venue.get(db, id=device_in.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    # Если запрошена генерация ключей, генерируем их и подставляем публичный ключ
    if device_in.generate_wireguard_keys:
        try:
            privkey, pubkey = generate_keypair()
            encrypted_priv = encrypt_secret(privkey)
            device_in.wireguard_pubkey = pubkey
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate WireGuard keys: {e}")
    else:
        encrypted_priv = None

    # Создание устройства
    device = crud_nas.create(db, obj_in=device_in)

    # Если генерировали ключи, обновляем приватный ключ
    if encrypted_priv:
        device.wireguard_private_key = encrypted_priv
        db.add(device)
        db.commit()

    # Создаём пир WireGuard, если есть публичный ключ
    if device.wireguard_pubkey:
        allowed_ips = f"192.168.99.{device.id + 1}/32"
        peer_in = WireGuardPeerCreate(
            nas_device_id=device.id,
            public_key=device.wireguard_pubkey,
            allowed_ips=allowed_ips,
            endpoint=f"{device.ip_address}:51820"
        )
        try:
            add_peer(peer_in.public_key, peer_in.allowed_ips, peer_in.endpoint)
            wireguard_peer.create(db, obj_in=peer_in)
        except Exception as e:
            crud_nas.remove(db, id=device.id)
            raise HTTPException(status_code=500, detail=f"Failed to add WireGuard peer: {str(e)}")

    return device

# Создание (без слеша)
@router.post("", response_model=NASDeviceOut)
def create_nas_device_without_slash(
    device_in: NASDeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать новое NAS-устройство (без слеша в URL)"""
    return create_nas_device(device_in, db, current_user)

# Получение по ID
@router.get("/{id}", response_model=NASDeviceOut)
def read_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    return device

# Обновление
@router.put("/{id}", response_model=NASDeviceOut)
def update_nas_device(
    id: int,
    device_in: NASDeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")

    # Если IP меняется, проверяем уникальность
    if device_in.ip_address and device_in.ip_address != device.ip_address:
        existing = db.query(NASDevice).filter(
            NASDevice.ip_address == device_in.ip_address,
            NASDevice.deleted_at.is_(None),
            NASDevice.id != id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="IP address already in use")

    # Проверка смены площадки
    if device_in.venue_id and device_in.venue_id != device.venue_id:
        venue = crud_venue.get(db, id=device_in.venue_id)
        if not venue:
            raise HTTPException(status_code=404, detail="New venue not found")

    device = crud_nas.update(db, db_obj=device, obj_in=device_in)
    return device

# Удаление
@router.delete("/{id}", response_model=NASDeviceOut)
def delete_nas_device(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    device = crud_nas.remove(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    return device

@router.get("/{id}/wireguard-private-key")
def get_wireguard_private_key(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Возвращает расшифрованный приватный ключ WireGuard для NAS."""
    device = crud_nas.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")

    # Проверка прав
    if current_user.is_superuser or current_user.role == 'admin' or current_user.role == 'support':
        pass
    elif current_user.role == 'venue_owner':
        if current_user.venue_id != device.venue_id:
            raise HTTPException(status_code=403, detail="Access denied")
        venue = db.get(Venue, device.venue_id)
        if not venue or not venue.allow_nas_connection_info:
            raise HTTPException(status_code=403, detail="NAS connection info is not allowed for this venue owner")
    else:
        raise HTTPException(status_code=403, detail="Access denied")

    if not device.wireguard_private_key:
        raise HTTPException(status_code=404, detail="No private key stored for this device")

    try:
        private_key = decrypt_secret(device.wireguard_private_key)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to decrypt private key")
    return {"private_key": private_key}