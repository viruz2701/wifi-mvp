from app.crud.base import CRUDBase
from app.models.sms_code import SMSCode
from app.schemas.sms_code import SMSCodeCreate, SMSCodeUpdate

class CRUDSMSCode(CRUDBase[SMSCode, SMSCodeCreate, SMSCodeUpdate]):
    def get_valid_code(self, db, phone: str, code: str):
        from datetime import datetime
        return db.query(self.model).filter(
            self.model.phone_number == phone,
            self.model.code == code,
            self.model.is_used == False,
            self.model.expires_at > datetime.utcnow(),
            self.model.deleted_at.is_(None)
        ).first()

sms_code = CRUDSMSCode(SMSCode)