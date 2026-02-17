from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Any, Dict
from app.models.sms_provider import SMSProviderType

class SMSProviderBase(BaseModel):
    name: str
    type: SMSProviderType
    config: Dict[str, Any]
    is_active: bool = True

class SMSProviderCreate(SMSProviderBase):
    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Название провайдера не может быть пустым')
        return v.strip()

    @validator('config')
    def config_not_empty(cls, v):
        if not v:
            raise ValueError('Конфигурация не может быть пустой')
        # Для RocketSMS можно проверить наличие обязательных ключей
        # Но это лучше делать в отдельном методе с учётом типа провайдера
        return v

class SMSProviderUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[SMSProviderType] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    @validator('name')
    def name_not_empty_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Название провайдера не может быть пустым')
        return v.strip() if v else v

    @validator('config')
    def config_not_empty_if_provided(cls, v):
        if v is not None and not v:
            raise ValueError('Конфигурация не может быть пустой')
        return v

class SMSProviderOut(SMSProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True