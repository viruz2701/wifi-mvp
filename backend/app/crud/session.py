from app.crud.base import CRUDBase
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate

class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):
    def get_active_by_mac(self, db, mac: str):
        return db.query(self.model).filter(
            self.model.mac_address == mac,
            self.model.is_active == True,
            self.model.deleted_at.is_(None)
        ).first()

session = CRUDSession(Session)