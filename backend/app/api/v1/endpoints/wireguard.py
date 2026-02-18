from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.wireguard_peer import wireguard_peer
from app.schemas.wireguard_peer import (
    WireGuardPeerCreate,
    WireGuardPeerUpdate,
    WireGuardPeerOut,
    WireGuardPeerWithNames
)
from app.core.dependencies import get_current_superuser
from app.core.wireguard import add_peer, remove_peer
from app.crud.nas_device import nas_device as crud_nas
from app.models.nas_device import NASDevice
from app.models.venue import Venue
from app.models.wireguard_peer import WireGuardPeer

router = APIRouter()

@router.get("", response_model=List[WireGuardPeerWithNames])
def read_peers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_superuser)
):
    """Получить список всех WireGuard пиров с названиями NAS и площадок."""
    # Выполняем запрос с джойнами
    results = db.query(
        WireGuardPeer,
        NASDevice.name.label('nas_name'),
        Venue.name.label('venue_name'),
        Venue.id.label('venue_id')
    ).join(
        NASDevice, WireGuardPeer.nas_device_id == NASDevice.id
    ).join(
        Venue, NASDevice.venue_id == Venue.id
    ).filter(
        WireGuardPeer.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()

    # Формируем список словарей, совместимых со схемой WireGuardPeerWithNames
    peers_list = []
    for peer, nas_name, venue_name, venue_id in results:
        peer_dict = {
            "id": peer.id,
            "nas_device_id": peer.nas_device_id,
            "public_key": peer.public_key,
            "allowed_ips": peer.allowed_ips,
            "endpoint": peer.endpoint,
            "is_active": peer.is_active,
            "created_at": peer.created_at,
            "updated_at": peer.updated_at,
            "nas_name": nas_name,
            "venue_name": venue_name,
            "venue_id": venue_id
        }
        peers_list.append(peer_dict)
    return peers_list

@router.post("", response_model=WireGuardPeerOut)
def create_peer(
    peer_in: WireGuardPeerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    nas_device = crud_nas.get(db, id=peer_in.nas_device_id)
    if not nas_device:
        raise HTTPException(status_code=404, detail="NAS device not found")

    existing = wireguard_peer.get_by_nas_device(db, peer_in.nas_device_id)
    if existing:
        raise HTTPException(status_code=400, detail="Peer already exists for this NAS device")

    peer = wireguard_peer.create(db, obj_in=peer_in)

    try:
        add_peer(peer.public_key, peer.allowed_ips, peer.endpoint)
    except Exception as e:
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
    peer = wireguard_peer.update(db, db_obj=peer, obj_in=peer_in)
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
    try:
        remove_peer(peer.public_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove peer from WireGuard: {e}")
    peer = wireguard_peer.remove(db, id=id)
    return peer