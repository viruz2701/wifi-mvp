from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict
from app.models.crm_provider import CRMProviderType

class CRMProviderBase(BaseModel):
    name: str
    type: CRMProviderType
    config: Dict[str, Any]
    is_active: bool = True
    priority: int = 0

class CRMProviderCreate(CRMProviderBase):
    pass

class CRMProviderUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CRMProviderType] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None

class CRMProviderOut(CRMProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True