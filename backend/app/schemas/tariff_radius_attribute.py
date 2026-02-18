from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .radius_attribute import RadiusAttributeOut

class TariffRadiusAttributeBase(BaseModel):
    tariff_id: int
    attribute_id: int
    value: str

class TariffRadiusAttributeCreate(TariffRadiusAttributeBase):
    pass

class TariffRadiusAttributeUpdate(BaseModel):
    value: Optional[str] = None

class TariffRadiusAttributeOut(TariffRadiusAttributeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TariffRadiusAttributeNested(BaseModel):
    id: int
    attribute: RadiusAttributeOut
    value: str

    class Config:
        from_attributes = True