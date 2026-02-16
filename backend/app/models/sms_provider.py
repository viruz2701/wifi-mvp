from sqlalchemy import Column, String, Boolean, JSON, Enum
from app.models.base import BaseModel
import enum

class SMSProviderType(str, enum.Enum):
    ROCKETSMS = "rocketsms"
    CALLPASSWORD = "callpassword"
    # другие по мере добавления

class SMSProvider(BaseModel):
    __tablename__ = "sms_providers"

    name = Column(String, nullable=False)          # человекочитаемое имя
    type = Column(Enum(SMSProviderType), nullable=False, default=SMSProviderType.ROCKETSMS)
    config = Column(JSON, nullable=False, default={})   # хранит все настройки (логин, пароль, отправитель и т.п.)
    is_active = Column(Boolean, default=True)