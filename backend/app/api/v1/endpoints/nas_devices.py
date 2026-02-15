from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.nas_device import nas_device as crud_nas
from app.crud.venue import venue as crud_venue
from app.crud.wireguard_peer import wireguard_peer
from app.schemas.nas_device import NASDeviceCreate, NASDeviceUpdate, NASDeviceOut
from app.schemas.wireguard_peer import WireGuardPeerCreate
from app.core.dependencies import get_current_superuser, get_current_active_user
from app.core.wireguard import add_peer
from app.models.user import User
from app.nas import get_nas_instance

router = APIRouter()


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
    
# Эндпоинт без слеша – для предотвращения редиректа
@router.get("", response_model=List[NASDeviceOut])
def read_nas_devices(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
):
    """Получить список всех NAS-устройств (доступно аутентифицированным пользователям)"""
    devices = crud_nas.get_multi(db, skip=skip, limit=limit)
    return devices

# Эндпоинт со слешем – для обратной совместимости
@router.get("/", response_model=List[NASDeviceOut])
def read_nas_devices_with_slash(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
):
    devices = crud_nas.get_multi(db, skip=skip, limit=limit)
    return devices

@router.post("/", response_model=NASDeviceOut)
def create_nas_device(
    device_in: NASDeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """Создать новое NAS-устройство (только суперпользователь)"""
    venue = crud_venue.get(db, id=device_in.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    device = crud_nas.create(db, obj_in=device_in)
    if device_in.wireguard_pubkey:
        allowed_ips = f"192.168.99.{device.id + 1}/32"
        peer_in = WireGuardPeerCreate(
            nas_device_id=device.id,
            public_key=device_in.wireguard_pubkey,
            allowed_ips=allowed_ips,
            endpoint=f"{device.ip_address}:51820"
        )
        try:
            add_peer(peer_in.public_key, peer_in.allowed_ips, peer_in.endpoint)
        except Exception as e:
            crud_nas.remove(db, id=device.id)
            raise HTTPException(status_code=500, detail=f"Failed to add WireGuard peer: {str(e)}")
        wireguard_peer.create(db, obj_in=peer_in)
    return device

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
    current_user: User = Depends(get_current_superuser),
):
    device = crud_nas.remove(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="NAS device not found")
    return device
