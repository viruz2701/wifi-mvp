from app.crud.base import CRUDBase
from app.models.wireguard_peer import WireGuardPeer
from app.schemas.wireguard_peer import WireGuardPeerCreate, WireGuardPeerUpdate

class CRUDWireGuardPeer(CRUDBase[WireGuardPeer, WireGuardPeerCreate, WireGuardPeerUpdate]):
    def get_by_nas_device(self, db, nas_device_id: int):
        return db.query(self.model).filter(
            self.model.nas_device_id == nas_device_id,
            self.model.deleted_at.is_(None)
        ).first()

wireguard_peer = CRUDWireGuardPeer(WireGuardPeer)