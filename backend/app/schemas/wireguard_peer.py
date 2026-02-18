from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WireGuardPeerBase(BaseModel):
    nas_device_id: int
    public_key: str
    allowed_ips: str
    endpoint: Optional[str] = None
    is_active: bool = True

class WireGuardPeerCreate(WireGuardPeerBase):
    pass

class WireGuardPeerUpdate(BaseModel):
    allowed_ips: Optional[str] = None
    endpoint: Optional[str] = None
    is_active: Optional[bool] = None

class WireGuardPeerOut(WireGuardPeerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WireGuardPeerWithNames(WireGuardPeerOut):
    nas_name: str
    venue_name: str
    venue_id: int