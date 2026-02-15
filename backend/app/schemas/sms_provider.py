from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SMSProviderBase(BaseModel):
    name: str
    api_url: str
    api_key: str
    sender: Optional[str] = None
    is_active: bool = True
    config: Optional[str] = None

class SMSProviderCreate(SMSProviderBase):
    pass

class SMSProviderUpdate(BaseModel):
    name: Optional[str] = None
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    sender: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[str] = None

class SMSProviderOut(SMSProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True