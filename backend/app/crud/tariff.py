from app.crud.base import CRUDBase
from app.models.tariff import TariffPlan
from app.schemas.tariff import TariffCreate, TariffUpdate

class CRUDTariff(CRUDBase[TariffPlan, TariffCreate, TariffUpdate]):
    pass

tariff = CRUDTariff(TariffPlan)