from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VenueBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    is_active: bool = True
    # Новые поля
    domain: Optional[str] = None
    ssl_enabled: bool = False

class VenueCreate(VenueBase):
    pass

class VenueUpdate(VenueBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    ssl_enabled: Optional[bool] = None

class VenueOut(VenueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True