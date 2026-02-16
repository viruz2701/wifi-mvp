from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.models.base import BaseModel
import enum

class CodeMethod(str, enum.Enum):
    SMS = "sms"
    CALL = "call"

class SMSCode(BaseModel):
    __tablename__ = "sms_codes"

    phone_number = Column(String(15), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    attempts = Column(Integer, default=0)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True)
    
    # Новые поля для звонков
    method = Column(Enum(CodeMethod), nullable=False, default=CodeMethod.SMS)
    call_id = Column(String, nullable=True)  # идентификатор звонка от провайдера
    provider_id = Column(Integer, ForeignKey("sms_providers.id"), nullable=True)
    
    def __repr__(self):
        return f"<SMSCode {self.phone_number} {self.code} method={self.method}>"