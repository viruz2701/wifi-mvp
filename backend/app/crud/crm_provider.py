from app.crud.base import CRUDBase
from app.models.crm_provider import CRMProvider
from app.schemas.crm_provider import CRMProviderCreate, CRMProviderUpdate

class CRUDCRMProvider(CRUDBase[CRMProvider, CRMProviderCreate, CRMProviderUpdate]):
    pass

crm_provider = CRUDCRMProvider(CRMProvider)