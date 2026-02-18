from app.crud.base import CRUDBase
from app.models.radius_attribute import RadiusAttribute
from app.schemas.radius_attribute import RadiusAttributeCreate, RadiusAttributeUpdate

class CRUDRadiusAttribute(CRUDBase[RadiusAttribute, RadiusAttributeCreate, RadiusAttributeUpdate]):
    def get_by_name(self, db, name: str):
        return db.query(self.model).filter(self.model.name == name).first()

radius_attribute = CRUDRadiusAttribute(RadiusAttribute)