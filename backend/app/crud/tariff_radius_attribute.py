from app.crud.base import CRUDBase
from app.models.tariff_radius_attribute import TariffRadiusAttribute
from app.schemas.tariff_radius_attribute import TariffRadiusAttributeCreate, TariffRadiusAttributeUpdate

class CRUDTariffRadiusAttribute(CRUDBase[TariffRadiusAttribute, TariffRadiusAttributeCreate, TariffRadiusAttributeUpdate]):
    def get_by_tariff(self, db, tariff_id: int):
        return db.query(self.model).filter(
            self.model.tariff_id == tariff_id,
            self.model.deleted_at.is_(None)
        ).all()

tariff_radius_attribute = CRUDTariffRadiusAttribute(TariffRadiusAttribute)