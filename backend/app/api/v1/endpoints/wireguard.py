from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.wireguard_peer import wireguard_peer
from app.schemas.wireguard_peer import WireGuardPeerCreate, WireGuardPeerUpdate, WireGuardPeerOut
from app.core.dependencies import get_current_superuser
from app.core.wireguard import add_peer, remove_peer

router = APIRouter()

@router.get("/", response_model=List[WireGuardPeerOut])
def read_peers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser)
):
    return wireguard_peer.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=WireGuardPeerOut)
def create_peer(
    peer_in: WireGuardPeerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    # Проверяем, нет ли уже пира для этого NASDevice
    existing = wireguard_peer.get_by_nas_device(db, peer_in.nas_device_id)
    if existing:
        raise HTTPException(status_code=400, detail="Peer already exists for this NAS device")
    # Создаём запись в БД
    peer = wireguard_peer.create(db, obj_in=peer_in)
    # Добавляем в WireGuard
    try:
        add_peer(peer.public_key, peer.allowed_ips, peer.endpoint)
    except Exception as e:
        # Если ошибка, удаляем запись из БД и возвращаем ошибку
        wireguard_peer.remove(db, id=peer.id)
        raise HTTPException(status_code=500, detail=f"Failed to add peer to WireGuard: {e}")
    return peer

@router.get("/{id}", response_model=WireGuardPeerOut)
def read_peer(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    peer = wireguard_peer.get(db, id=id)
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found")
    return peer

@router.put("/{id}", response_model=WireGuardPeerOut)
def update_peer(
    id: int,
    peer_in: WireGuardPeerUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    peer = wireguard_peer.get(db, id=id)
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found")
    # Обновляем в БД
    peer = wireguard_peer.update(db, db_obj=peer, obj_in=peer_in)
    # В реальном обновлении WireGuard нужно удалить старый пир и добавить заново, если изменился ключ или allowed_ips.
    # Для простоты реализуем только обновление allowed_ips и endpoint через повторное добавление.
    # Упростим: удалим и добавим заново.
    try:
        remove_peer(peer.public_key)
        add_peer(peer.public_key, peer.allowed_ips, peer.endpoint)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update peer in WireGuard: {e}")
    return peer

@router.delete("/{id}", response_model=WireGuardPeerOut)
def delete_peer(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    peer = wireguard_peer.get(db, id=id)
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found")
    # Удаляем из WireGuard
    try:
        remove_peer(peer.public_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove peer from WireGuard: {e}")
    # Мягкое удаление в БД
    peer = wireguard_peer.remove(db, id=id)
    return peer