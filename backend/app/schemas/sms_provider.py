from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict
from app.models.sms_provider import SMSProviderType

class SMSProviderBase(BaseModel):
    name: str
    type: SMSProviderType
    config: Dict[str, Any] = {}
    is_active: bool = True

class SMSProviderCreate(SMSProviderBase):
    pass

class SMSProviderUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[SMSProviderType] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class SMSProviderOut(SMSProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True