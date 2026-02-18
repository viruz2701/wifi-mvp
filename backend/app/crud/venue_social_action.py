from app.crud.base import CRUDBase
from app.models.venue_social_action import VenueSocialAction
from app.schemas.venue_social_action import VenueSocialActionCreate, VenueSocialActionUpdate

class CRUDVenueSocialAction(CRUDBase[VenueSocialAction, VenueSocialActionCreate, VenueSocialActionUpdate]):
    def get_by_venue(self, db, venue_id: int):
        return db.query(self.model).filter(
            self.model.venue_id == venue_id,
            self.model.deleted_at.is_(None)
        ).all()

venue_social_action = CRUDVenueSocialAction(VenueSocialAction)