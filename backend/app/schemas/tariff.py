from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TariffBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "RUB"
    duration_hours: int
    speed_limit_up_kbps: Optional[int] = None
    speed_limit_down_kbps: Optional[int] = None
    is_active: bool = True

class TariffCreate(TariffBase):
    pass

class TariffUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    duration_hours: Optional[int] = None
    speed_limit_up_kbps: Optional[int] = None
    speed_limit_down_kbps: Optional[int] = None
    is_active: Optional[bool] = None

class TariffOut(TariffBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True