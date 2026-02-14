from app.crud.base import CRUDBase
from app.models.sms_provider import SMSProvider
from app.schemas.sms_provider import SMSProviderCreate, SMSProviderUpdate

class CRUDSMSProvider(CRUDBase[SMSProvider, SMSProviderCreate, SMSProviderUpdate]):
    pass

sms_provider = CRUDSMSProvider(SMSProvider)