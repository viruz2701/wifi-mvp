# backend/app/models/sms_provider.py
from sqlalchemy import Column, String, Boolean, JSON, Enum, Integer
from app.models.base import BaseModel
import enum

class SMSProviderType(str, enum.Enum):
    ROCKETSMS = "rocketsms"
    CALLPASSWORD = "callpassword"
    WEBSMS = "websms"  # <-- новый тип

class SMSProvider(BaseModel):
    __tablename__ = "sms_providers"

    name = Column(String, nullable=False)
    type = Column(Enum(SMSProviderType), nullable=False, default=SMSProviderType.ROCKETSMS)
    config = Column(JSON, nullable=False, default={})
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # порядок использования