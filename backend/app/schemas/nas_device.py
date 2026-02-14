from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.nas_device import NASDeviceType

class NASDeviceBase(BaseModel):
    venue_id: int
    name: str
    type: NASDeviceType
    ip_address: str
    api_username: Optional[str] = None
    wireguard_pubkey: Optional[str] = None
    wireguard_ip: Optional[str] = None
    is_active: bool = True

class NASDeviceCreate(NASDeviceBase):
    secret: str  # открытый секрет для шифрования
    api_password: Optional[str] = None

class NASDeviceUpdate(NASDeviceBase):
    secret: Optional[str] = None
    api_password: Optional[str] = None

class NASDeviceOut(NASDeviceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True