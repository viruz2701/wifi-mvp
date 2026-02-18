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
    domain: Optional[str] = None
    ssl_enabled: bool = False
    # Новые поля
    crm_enabled: bool = False
    show_email_field: bool = False
    show_name_field: bool = False
    show_marketing_consent: bool = False
    allow_nas_connection_info: bool = False

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    is_active: Optional[bool] = None
    domain: Optional[str] = None
    ssl_enabled: Optional[bool] = None
    # Новые поля (опциональны при обновлении)
    crm_enabled: Optional[bool] = None
    show_email_field: Optional[bool] = None
    show_name_field: Optional[bool] = None
    show_marketing_consent: Optional[bool] = None
    allow_nas_connection_info: Optional[bool] = None

class VenueOut(VenueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True