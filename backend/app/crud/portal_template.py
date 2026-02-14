from app.crud.base import CRUDBase
from app.models.portal_template import PortalTemplate
from app.schemas.portal_template import PortalTemplateCreate, PortalTemplateUpdate

class CRUDPortalTemplate(CRUDBase[PortalTemplate, PortalTemplateCreate, PortalTemplateUpdate]):
    def get_active_by_venue_and_type(self, db, venue_id: int, type: str):
        return db.query(self.model).filter(
            self.model.venue_id == venue_id,
            self.model.type == type,
            self.model.is_active == True,
            self.model.deleted_at.is_(None)
        ).first()

portal_template = CRUDPortalTemplate(PortalTemplate)